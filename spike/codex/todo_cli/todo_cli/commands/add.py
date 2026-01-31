"""タスク追加コマンドの実装。"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models import Task, now_iso_utc
from ..storage import load_tasks, save_tasks

VALID_PRIORITIES = {"high", "medium", "low"}


def _normalize_categories(categories: Optional[list[str]]) -> list[str]:
    if not categories:
        return []
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


def add_task(
    storage_path: Path,
    title: str,
    *,
    description: Optional[str] = None,
    priority: str,
    due_date: Optional[str] = None,
    categories: Optional[list[str]] = None,
) -> Task:
    """タスクを追加して永続化し、追加したタスクを返す。"""
    if not title or not title.strip():
        raise ValueError("title is required")
    if priority not in VALID_PRIORITIES:
        raise ValueError("priority must be high, medium, or low")
    _validate_due_date(due_date)

    task = Task(
        id=str(uuid.uuid4()),
        title=title.strip(),
        description=description,
        priority=priority,  # type: ignore[arg-type]
        due_date=due_date,
        categories=_normalize_categories(categories),
        status="open",
        created_at=now_iso_utc(),
        completed_at=None,
    )

    tasks = load_tasks(storage_path)
    tasks.append(task)
    save_tasks(storage_path, tasks)
    return task
