"""タスク完了コマンドの実装。"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from ..models import Task, now_iso_utc
from ..storage import load_tasks, save_tasks


def _set_done(task: Task) -> Task:
    return replace(task, status="done", completed_at=now_iso_utc())


def mark_done(storage_path: Path, task_id: str) -> Task:
    """指定タスクを完了状態に更新して返す。"""
    tasks = load_tasks(storage_path)
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated = _set_done(task)
            tasks[idx] = updated
            save_tasks(storage_path, tasks)
            return updated
    raise ValueError("task id not found")
