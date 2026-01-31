"""edit コマンドのテスト。"""

from __future__ import annotations

from pathlib import Path

import pytest

from todo_cli.commands.edit import edit_task
from todo_cli.models import Task
from todo_cli.storage import load_tasks, save_tasks


def _make_task(*, task_id: str) -> Task:
    return Task(
        id=task_id,
        title="Write spec",
        description=None,
        priority="medium",  # type: ignore[arg-type]
        due_date=None,
        categories=["work"],
        status="open",  # type: ignore[arg-type]
        created_at="2026-01-01T10:00:00Z",
        completed_at=None,
    )


def test_edit_updates_fields(tmp_path: Path) -> None:
    """複数フィールドが更新できることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [_make_task(task_id="1")])

    updated = edit_task(
        storage_path,
        "1",
        title="Prepare slides",
        description="For kickoff",
        priority="high",
        due_date="2026-02-10",
        categories=["Work", "Work", "Meetings"],
    )

    assert updated.title == "Prepare slides"
    assert updated.description == "For kickoff"
    assert updated.priority == "high"
    assert updated.due_date == "2026-02-10"
    assert updated.categories == ["work", "meetings"]

    stored = load_tasks(storage_path)[0]
    assert stored.title == "Prepare slides"


def test_edit_partial_update(tmp_path: Path) -> None:
    """一部フィールドのみ更新できることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [_make_task(task_id="1")])

    updated = edit_task(storage_path, "1", priority="low")

    assert updated.priority == "low"
    assert updated.title == "Write spec"


def test_edit_invalid_title(tmp_path: Path) -> None:
    """空タイトルはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [_make_task(task_id="1")])

    with pytest.raises(ValueError, match="title is required"):
        edit_task(storage_path, "1", title=" ")


def test_edit_invalid_priority(tmp_path: Path) -> None:
    """不正な優先度はエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [_make_task(task_id="1")])

    with pytest.raises(ValueError, match="priority"):
        edit_task(storage_path, "1", priority="urgent")


def test_edit_invalid_due_date(tmp_path: Path) -> None:
    """不正な期限形式はエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [_make_task(task_id="1")])

    with pytest.raises(ValueError):
        edit_task(storage_path, "1", due_date="2026/02/10")


def test_edit_not_found(tmp_path: Path) -> None:
    """存在しないIDはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [])

    with pytest.raises(ValueError, match="task id not found"):
        edit_task(storage_path, "missing", title="New title")
