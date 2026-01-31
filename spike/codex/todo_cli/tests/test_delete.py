"""delete コマンドのテスト。"""

from __future__ import annotations

from pathlib import Path

import pytest

from todo_cli.commands.delete import delete_task
from todo_cli.models import Task
from todo_cli.storage import load_tasks, save_tasks


def _make_task(*, task_id: str) -> Task:
    return Task(
        id=task_id,
        title="Task",
        description=None,
        priority="medium",  # type: ignore[arg-type]
        due_date=None,
        categories=[],
        status="open",  # type: ignore[arg-type]
        created_at="2026-01-01T10:00:00Z",
        completed_at=None,
    )


def test_delete_task(tmp_path: Path) -> None:
    """指定IDの削除ができることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [_make_task(task_id="1"), _make_task(task_id="2")]
    save_tasks(storage_path, tasks)

    deleted = delete_task(storage_path, "1")

    assert deleted.id == "1"
    remaining = load_tasks(storage_path)
    assert [task.id for task in remaining] == ["2"]


def test_delete_not_found(tmp_path: Path) -> None:
    """存在しないIDはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [])

    with pytest.raises(ValueError, match="task id not found"):
        delete_task(storage_path, "missing")
