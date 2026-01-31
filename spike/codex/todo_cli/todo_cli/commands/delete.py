"""タスク削除コマンドの実装。"""

from __future__ import annotations

from pathlib import Path

from ..models import Task
from ..storage import load_tasks, save_tasks


def delete_task(storage_path: Path, task_id: str) -> Task:
    """指定タスクを削除して返す。"""
    tasks = load_tasks(storage_path)
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            deleted = tasks.pop(idx)
            save_tasks(storage_path, tasks)
            return deleted
    raise ValueError("task id not found")
