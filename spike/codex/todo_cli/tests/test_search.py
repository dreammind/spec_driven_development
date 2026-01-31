"""search コマンドのテスト。"""

from __future__ import annotations

from pathlib import Path

import pytest

from todo_cli.commands.search import search_tasks
from todo_cli.models import Task
from todo_cli.storage import save_tasks


def _make_task(*, task_id: str, title: str, description: str | None) -> Task:
    return Task(
        id=task_id,
        title=title,
        description=description,
        priority="medium",  # type: ignore[arg-type]
        due_date=None,
        categories=[],
        status="open",  # type: ignore[arg-type]
        created_at="2026-01-01T10:00:00Z",
        completed_at=None,
    )


def test_search_matches_title_and_description(tmp_path: Path) -> None:
    """タイトル/説明の一致を確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(task_id="1", title="Write spec", description=None),
        _make_task(task_id="2", title="Prepare slides", description="Kickoff meeting"),
    ]
    save_tasks(storage_path, tasks)

    by_title = search_tasks(storage_path, "spec")
    assert [task.id for task in by_title] == ["1"]

    by_description = search_tasks(storage_path, "meeting")
    assert [task.id for task in by_description] == ["2"]


def test_search_partial_match_case_insensitive(tmp_path: Path) -> None:
    """部分一致と大文字小文字無視を確認する。"""
    storage_path = tmp_path / "tasks.json"
    tasks = [
        _make_task(task_id="1", title="Write Spec", description=None),
        _make_task(task_id="2", title="Prepare slides", description="Kickoff meeting"),
    ]
    save_tasks(storage_path, tasks)

    results = search_tasks(storage_path, "spe")
    assert [task.id for task in results] == ["1"]


def test_search_empty_keyword_raises(tmp_path: Path) -> None:
    """空キーワードはエラーになることを確認する。"""
    storage_path = tmp_path / "tasks.json"
    save_tasks(storage_path, [])

    with pytest.raises(ValueError, match="keyword is required"):
        search_tasks(storage_path, "   ")
