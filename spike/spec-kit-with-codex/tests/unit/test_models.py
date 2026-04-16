from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from todo_cli.models import TASK_TITLE_MAX_LENGTH, Task


def test_task_title_trimmed_and_valid() -> None:
    task = Task(id=uuid4(), title="  buy milk  ")
    assert task.title == "buy milk"


def test_task_empty_title_rejected() -> None:
    with pytest.raises(ValidationError):
        Task(id=uuid4(), title="   ")


def test_task_too_long_title_rejected() -> None:
    with pytest.raises(ValidationError):
        Task(id=uuid4(), title="x" * (TASK_TITLE_MAX_LENGTH + 1))


def test_task_restore_resets_completion() -> None:
    task = Task(id=uuid4(), title="x", is_completed=True, is_archived=True)
    restored = task.restore()
    assert restored.is_archived is False
    assert restored.is_completed is False


def test_task_created_at_default_is_timezone_aware() -> None:
    task = Task(id=uuid4(), title="x")
    assert isinstance(task.created_at, datetime)
    assert task.created_at.tzinfo == UTC
