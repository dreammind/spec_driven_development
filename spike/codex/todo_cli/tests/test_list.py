"""list コマンドのテスト。"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from todo_cli.commands.list import list_tasks
from todo_cli.models import Task
from todo_cli.storage import save_tasks


def _make_task(
    *,
    task_id: str,
    title: str,
    priority: str,
    status: str,
    created_at: str,
    due_date: str | None = None,
    categories: list[str] | None = None,
) -> Task:
    return Task(
        id=task_id,
        title=title,
        description=None,
        priority=priority,  # type: ignore[arg-type]
        due_date=due_date,
        categories=categories or [],
        status=status,  # type: ignore[arg-type]
        created_at=created_at,
        completed_at=None,
    )


def test_list_all(tmp_path: Path) -> None:
    """全タスクが表示されることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(
            task_id="1",
            title="Write spec",
            priority="high",
            status="open",
            created_at="2026-01-01T10:00:00Z",
        ),
        _make_task(
            task_id="2",
            title="Review",
            priority="low",
            status="done",
            created_at="2026-01-02T10:00:00Z",
        ),
    ]
    save_tasks(storage_path, tasks)

    result = list_tasks(storage_path)

    assert [task.id for task in result] == ["1", "2"]


def test_list_filter_status(tmp_path: Path) -> None:
    """status フィルタが動作することを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(
            task_id="1",
            title="Write spec",
            priority="high",
            status="open",
            created_at="2026-01-01T10:00:00Z",
        ),
        _make_task(
            task_id="2",
            title="Review",
            priority="low",
            status="done",
            created_at="2026-01-02T10:00:00Z",
        ),
    ]
    save_tasks(storage_path, tasks)

    result = list_tasks(storage_path, status="done")

    assert [task.id for task in result] == ["2"]


def test_list_filter_priority_and_category(tmp_path: Path) -> None:
    """priority と category の複合フィルタを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(
            task_id="1",
            title="Write spec",
            priority="high",
            status="open",
            created_at="2026-01-01T10:00:00Z",
            categories=["work"],
        ),
        _make_task(
            task_id="2",
            title="Grocery",
            priority="high",
            status="open",
            created_at="2026-01-02T10:00:00Z",
            categories=["personal"],
        ),
        _make_task(
            task_id="3",
            title="Review",
            priority="low",
            status="open",
            created_at="2026-01-03T10:00:00Z",
            categories=["work"],
        ),
    ]
    save_tasks(storage_path, tasks)

    result = list_tasks(storage_path, priority="high", category="Work")

    assert [task.id for task in result] == ["1"]


def test_list_sort_due_priority_created(tmp_path: Path) -> None:
    """sort オプションの並び順を確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(
            task_id="1",
            title="No due",
            priority="low",
            status="open",
            created_at="2026-01-03T10:00:00Z",
        ),
        _make_task(
            task_id="2",
            title="Due later",
            priority="medium",
            status="open",
            created_at="2026-01-02T10:00:00Z",
            due_date="2026-02-10",
        ),
        _make_task(
            task_id="3",
            title="Due sooner",
            priority="high",
            status="open",
            created_at="2026-01-01T10:00:00Z",
            due_date="2026-02-05",
        ),
    ]
    save_tasks(storage_path, tasks)

    by_due = list_tasks(storage_path, sort="due")
    assert [task.id for task in by_due] == ["3", "2", "1"]

    by_priority = list_tasks(storage_path, sort="priority")
    assert [task.id for task in by_priority] == ["3", "2", "1"]

    by_created = list_tasks(storage_path, sort="created")
    assert [task.id for task in by_created] == ["3", "2", "1"]


def test_list_overdue(tmp_path: Path) -> None:
    """overdue オプションが期限切れのみ返すことを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(
            task_id="1",
            title="Overdue",
            priority="high",
            status="open",
            created_at="2026-01-01T10:00:00Z",
            due_date="2026-01-01",
        ),
        _make_task(
            task_id="2",
            title="Future",
            priority="high",
            status="open",
            created_at="2026-01-02T10:00:00Z",
            due_date="2026-02-01",
        ),
    ]
    save_tasks(storage_path, tasks)

    result = list_tasks(storage_path, overdue=True, today=date(2026, 1, 31))

    assert [task.id for task in result] == ["1"]


def test_list_invalid_filters(tmp_path: Path) -> None:
    """不正なフィルタ値はエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [])

    with pytest.raises(ValueError, match="status"):
        list_tasks(storage_path, status="invalid")

    with pytest.raises(ValueError, match="priority"):
        list_tasks(storage_path, priority="urgent")

    with pytest.raises(ValueError, match="sort"):
        list_tasks(storage_path, sort="unknown")
