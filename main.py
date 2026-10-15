"""
タスク管理API（FastAPI + SQLAlchemy + SQLite）
"""
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ==========================================
# Pydanticモデル
# ==========================================

class TaskCreate(BaseModel):
    """タスク作成時のリクエストモデル"""
    title: str
    completed: bool = False

class Task(BaseModel):
    """タスク情報のレスポンスモデル"""
    id: int
    title: str
    completed: bool
    created_at: datetime

# ==========================================
# インメモリのデータ置き場（Phase 4 でDBに置き換える）
# ==========================================

tasks: list[Task] = []
next_id: int = 1

# ==========================================
# エンドポイント
# ==========================================

app = FastAPI(title="タスク管理API", version="1.0.0")

@app.get("/tasks", response_model=list[Task])
def read_tasks():
    """
    タスク一覧を取得

    Returns:
    - タスク一覧（JSON配列）
    """
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    """
    タスク１件を取得

    Args:
    - task_id: 取得対象のタスクID

    Returns:
    - タスク1件（JSON）

    Raises:
    - HTTPException: タスクが見つからない場合は404
    """
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    """
    タスクを新規作成

    Args:
    - payload: 検証済みの入力（不正な入力は422）

    Returns:
    - 登録したタスク（201）
    """
    global next_id
    task = Task(
        id=next_id,
        title=payload.title,
        completed=payload.completed,
        created_at=datetime.now(timezone.utc),
    )
    next_id += 1
    tasks.append(task)
    return task
