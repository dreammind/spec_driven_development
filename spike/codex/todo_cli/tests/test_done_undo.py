"""done/undo コマンドのテスト。"""

from __future__ import annotations

from pathlib import Path

import pytest

from todo_cli.commands.done import mark_done
from todo_cli.commands.undo import mark_open
from todo_cli.models import Task
from todo_cli.storage import load_tasks, save_tasks


def _make_task(*, task_id: str, status: str, completed_at: str | None) -> Task:
    return Task(
        id=task_id,
        title="Task",
        description=None,
        priority="medium",  # type: ignore[arg-type]
        due_date=None,
        categories=[],
        status=status,  # type: ignore[arg-type]
        created_at="2026-01-01T10:00:00Z",
        completed_at=completed_at,
    )


def test_mark_done_sets_completed_at(tmp_path: Path) -> None:
    """done で完了状態と完了日時が設定されることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [_make_task(task_id="1", status="open", completed_at=None)]
    save_tasks(storage_path, tasks)

    updated = mark_done(storage_path, "1")

    assert updated.status == "done"
    assert updated.completed_at is not None

    stored = load_tasks(storage_path)[0]
    assert stored.status == "done"
    assert stored.completed_at is not None


def test_mark_open_clears_completed_at(tmp_path: Path) -> None:
    """undo で未完了と完了日時クリアを確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [_make_task(task_id="1", status="done", completed_at="2026-01-01T10:05:00Z")]
    save_tasks(storage_path, tasks)

    updated = mark_open(storage_path, "1")

    assert updated.status == "open"
    assert updated.completed_at is None

    stored = load_tasks(storage_path)[0]
    assert stored.status == "open"
    assert stored.completed_at is None


def test_mark_done_not_found(tmp_path: Path) -> None:
    """存在しないIDはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [])

    with pytest.raises(ValueError, match="task id not found"):
        mark_done(storage_path, "missing")


def test_mark_open_not_found(tmp_path: Path) -> None:
    """存在しないIDはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [])

    with pytest.raises(ValueError, match="task id not found"):
        mark_open(storage_path, "missing")
