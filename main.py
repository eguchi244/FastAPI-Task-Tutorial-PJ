"""
タスク管理API（FastAPI + SQLAlchemy + SQLite）
"""
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ==========================================
# Pydanticモデル
# ==========================================

class TaskCreate(BaseModel):
    """タスク作成時のリクエストモデル"""
    title: str = Field(..., min_length=1, max_length=255)
    completed: bool = False

class TaskUpdate(BaseModel):
    """タスク更新時のリクエストモデル"""
    title: str | None = Field(None, min_length=1, max_length=255)
    completed: bool | None = None

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
# ヘルパー関数
# ==========================================

def get_task(task_id: int) -> Task:
    """
    指定されたIDのタスクを取得する

    Args:
        task_id (int): 検索対象のタスクID

    Returns:
        Task: 見つかったタスクオブジェクト

    Raises:
        HTTPException: タスクが見つからない場合（404 Task Not Found）
    """
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# ==========================================
# エンドポイント
# ==========================================

app = FastAPI(title="タスク管理API", version="1.0.0")

@app.get("/tasks", response_model=list[Task])
def read_tasks(completed: bool | None = None):
    """
    タスク一覧（?completed=true/false で絞り込み可）

    Args:
    - completed: 完了状態での絞り込み（省略時は全件）

    Returns:
    - タスク一覧（JSON配列）
    """

    # 絞り込みがない場合（?completed=None, 省略）はすべてのタスクを返す
    if completed is None:
        return tasks

    # 絞り込みがある場合（?completed=true/false）はcompletedが一致するものだけ返す
    return [task for task in tasks if task.completed == completed]

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
    return get_task(task_id)

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

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    """
    タスクを更新（渡された項目のみ反映する部分更新）

    Args:
    - task_id: 更新対象のタスクID
    - payload: 検証済みの入力（None の項目は変更しない。不正な入力は422）

    Returns:
    - 更新したタスク

    Raises:
    - HTTPException: タスクが見つからない場合は404
    """
    task = get_task(task_id)

    if payload.title is not None:
        task.title = payload.title
    if payload.completed is not None:
        task.completed = payload.completed

    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    タスクを削除

    Args:
    - task_id: 削除対象のタスクID

    Returns:
    - 削除できたことを示す {"ok": true}

    Raises:
    - HTTPException: タスクが見つからない場合は404
    """
    task = get_task(task_id)
    tasks.remove(task)
    return {"ok": True}

