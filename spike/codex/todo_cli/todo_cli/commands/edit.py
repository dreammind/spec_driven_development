"""タスク編集コマンドの実装。"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models import Task
from ..storage import load_tasks, save_tasks

VALID_PRIORITIES = {"high", "medium", "low"}


def _normalize_categories(categories: Optional[list[str]]) -> Optional[list[str]]:
    if categories is None:
        return None
    normalized = []
    seen = set()
    for cat in categories:
        key = cat.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        normalized.append(key)
    return normalized


def _validate_due_date(due_date: Optional[str]) -> None:
    if due_date is None:
        return
    datetime.strptime(due_date, "%Y-%m-%d")


def edit_task(
    storage_path: Path,
    task_id: str,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    categories: Optional[list[str]] = None,
) -> Task:
    """指定タスクを編集して返す。"""
    if title is not None and not title.strip():
        raise ValueError("title is required")
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError("priority must be high, medium, or low")
    _validate_due_date(due_date)

    tasks = load_tasks(storage_path)
    for idx, task in enumerate(tasks):
        if task.id != task_id:
            continue
        updated = task
        if title is not None:
            updated = replace(updated, title=title.strip())
        if description is not None:
            updated = replace(updated, description=description)
        if priority is not None:
            updated = replace(updated, priority=priority)  # type: ignore[arg-type]
        if due_date is not None:
            updated = replace(updated, due_date=due_date)
        if categories is not None:
            updated = replace(updated, categories=_normalize_categories(categories) or [])
        tasks[idx] = updated
        save_tasks(storage_path, tasks)
        return updated
    raise ValueError("task id not found")
