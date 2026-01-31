"""タスク取り消しコマンドの実装。"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from ..models import Task
from ..storage import load_tasks, save_tasks


def _set_open(task: Task) -> Task:
    return replace(task, status="open", completed_at=None)


def mark_open(storage_path: Path, task_id: str) -> Task:
    """指定タスクを未完了状態に戻して返す。"""
    tasks = load_tasks(storage_path)
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated = _set_open(task)
            tasks[idx] = updated
            save_tasks(storage_path, tasks)
            return updated
    raise ValueError("task id not found")
