"""
タスク管理API（FastAPI + SQLAlchemy + SQLite）
"""
from fastapi import FastAPI

app = FastAPI(title="タスク管理API", version="1.0.0")

@app.get("/tasks")
def read_tasks():
    """
    タスク一覧を取得

    Returns:
    - list: タスクオブジェクトのリスト
    """
    return []
