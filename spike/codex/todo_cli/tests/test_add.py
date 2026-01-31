"""add コマンドのテスト。"""

from pathlib import Path

import pytest

from todo_cli.commands.add import add_task
from todo_cli.storage import load_tasks


def test_add_minimal(tmp_path: Path) -> None:
    """必須項目のみで追加できることを確認する。"""
    storage_path = tmp_path / "tasks.json"

    task = add_task(storage_path, "Write spec", priority="high")

    tasks = load_tasks(storage_path)
    assert len(tasks) == 1
    stored = tasks[0]
    assert stored.id == task.id
    assert stored.title == "Write spec"
    assert stored.description is None
    assert stored.priority == "high"
    assert stored.due_date is None
    assert stored.categories == []
    assert stored.status == "open"
    assert stored.completed_at is None


def test_add_with_optional_fields(tmp_path: Path) -> None:
    """任意項目を含めて追加できることを確認する。"""
    storage_path = tmp_path / "tasks.json"

    task = add_task(
        storage_path,
        "Prepare slides",
        description="For kickoff",
        priority="medium",
        due_date="2026-02-10",
        categories=["Work", "work", "Meetings"],
    )

    tasks = load_tasks(storage_path)
    assert len(tasks) == 1
    stored = tasks[0]
    assert stored.id == task.id
    assert stored.description == "For kickoff"
    assert stored.due_date == "2026-02-10"
    assert stored.categories == ["work", "meetings"]


def test_add_empty_title_raises(tmp_path: Path) -> None:
    """空タイトルはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"

    with pytest.raises(ValueError, match="title is required"):
        add_task(storage_path, "   ", priority="high")


def test_add_invalid_priority_raises(tmp_path: Path) -> None:
    """不正な優先度はエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"

    with pytest.raises(ValueError, match="priority"):
        add_task(storage_path, "Write spec", priority="urgent")


def test_add_invalid_due_date_raises(tmp_path: Path) -> None:
    """不正な期限形式はエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"

    with pytest.raises(ValueError):
        add_task(storage_path, "Write spec", priority="high", due_date="2026/02/10")
