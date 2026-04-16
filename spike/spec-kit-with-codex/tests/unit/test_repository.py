from __future__ import annotations

from pathlib import Path

import pytest

from todo_cli.repository import (
    InvalidTaskIdError,
    TaskAlreadyArchivedError,
    TaskNotArchivedError,
    TaskNotFoundError,
    TaskRepository,
    TaskValidationError,
)


def test_add_and_list_default_filters_completed_and_archived(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    t1 = repo.add_task("task1")
    t2 = repo.add_task("task2")
    repo.complete_task(str(t2.id))
    repo.archive_task(str(t2.id))

    listed = repo.list_tasks()
    assert [t.id for t in listed] == [t1.id]


def test_add_empty_title_raises_validation(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    with pytest.raises(TaskValidationError):
        repo.add_task(" ")


def test_invalid_id_raises(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    with pytest.raises(InvalidTaskIdError):
        repo.complete_task("not-uuid")


def test_missing_id_raises(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    with pytest.raises(TaskNotFoundError):
        repo.complete_task("cb5f4da4-8ba6-4ce9-9b58-849534f4f5d3")


def test_archive_twice_raises(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    task = repo.add_task("task")
    repo.archive_task(str(task.id))
    with pytest.raises(TaskAlreadyArchivedError):
        repo.archive_task(str(task.id))


def test_restore_non_archived_raises(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    task = repo.add_task("task")
    with pytest.raises(TaskNotArchivedError):
        repo.restore_task(str(task.id))


def test_restore_sets_incomplete(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "tasks.json")
    task = repo.add_task("task")
    repo.complete_task(str(task.id))
    repo.archive_task(str(task.id))
    restored = repo.restore_task(str(task.id))
    assert restored.is_archived is False
    assert restored.is_completed is False
