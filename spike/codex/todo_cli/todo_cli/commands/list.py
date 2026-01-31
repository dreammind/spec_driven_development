"""タスク一覧表示コマンドの実装。"""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, Optional

from ..models import Task
from ..storage import load_tasks

_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _parse_datetime(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _filter_status(tasks: Iterable[Task], status: str) -> list[Task]:
    if status == "all":
        return list(tasks)
    return [task for task in tasks if task.status == status]


def _filter_priority(tasks: Iterable[Task], priority: Optional[str]) -> list[Task]:
    if priority is None:
        return list(tasks)
    return [task for task in tasks if task.priority == priority]


def _filter_category(tasks: Iterable[Task], category: Optional[str]) -> list[Task]:
    if category is None:
        return list(tasks)
    key = category.strip().lower()
    if not key:
        return list(tasks)
    return [task for task in tasks if key in task.categories]


def _filter_overdue(tasks: Iterable[Task], today: date) -> list[Task]:
    overdue: list[Task] = []
    for task in tasks:
        if task.due_date is None:
            continue
        if _parse_date(task.due_date) < today:
            overdue.append(task)
    return overdue


def _sort_tasks(tasks: list[Task], sort_key: Optional[str]) -> list[Task]:
    if sort_key is None:
        return tasks
    if sort_key == "due":
        return sorted(
            tasks,
            key=lambda task: (
                0 if task.due_date is not None else 1,
                task.due_date or "",
            ),
        )
    if sort_key == "priority":
        return sorted(tasks, key=lambda task: _PRIORITY_ORDER.get(task.priority, 99))
    if sort_key == "created":
        return sorted(tasks, key=lambda task: _parse_datetime(task.created_at))
    raise ValueError("sort must be due, priority, or created")


def list_tasks(
    storage_path: Path,
    *,
    status: str = "all",
    priority: Optional[str] = None,
    category: Optional[str] = None,
    sort: Optional[str] = None,
    overdue: bool = False,
    today: Optional[date] = None,
) -> list[Task]:
    """フィルタ/ソート条件に基づきタスク一覧を返す。"""
    if status not in {"all", "open", "done"}:
        raise ValueError("status must be all, open, or done")
    if priority is not None and priority not in {"high", "medium", "low"}:
        raise ValueError("priority must be high, medium, or low")

    tasks = load_tasks(storage_path)
    results = _filter_status(tasks, status)
    results = _filter_priority(results, priority)
    results = _filter_category(results, category)

    if overdue:
        results = _filter_overdue(results, today or date.today())

    results = _sort_tasks(results, sort)
    return results
