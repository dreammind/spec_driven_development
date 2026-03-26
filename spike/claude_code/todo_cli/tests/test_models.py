from datetime import date, datetime

import pytest

from todo_cli.models import Priority, Task


class TestPriority:
    def test_values_exist(self) -> None:
        assert Priority.HIGH == "high"
        assert Priority.MEDIUM == "medium"
        assert Priority.LOW == "low"

    def test_from_string(self) -> None:
        assert Priority("high") == Priority.HIGH
        assert Priority("medium") == Priority.MEDIUM
        assert Priority("low") == Priority.LOW

    def test_invalid_value(self) -> None:
        with pytest.raises(ValueError):
            Priority("invalid")


class TestTask:
    def _make_task(self, **kwargs: object) -> Task:
        defaults = {
            "title": "テストタスク",
        }
        defaults.update(kwargs)
        return Task.create(title=str(defaults["title"]))

    def test_required_fields(self) -> None:
        task = Task.create(title="テスト")
        assert task.id != ""
        assert task.title == "テスト"
        assert task.done is False
        assert task.priority == Priority.MEDIUM
        assert task.due_date is None
        assert task.category is None
        assert task.deleted_at is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_default_done_is_false(self) -> None:
        task = Task.create(title="タスク")
        assert task.done is False

    def test_default_priority_is_medium(self) -> None:
        task = Task.create(title="タスク")
        assert task.priority == Priority.MEDIUM

    def test_optional_fields_default_none(self) -> None:
        task = Task.create(title="タスク")
        assert task.due_date is None
        assert task.category is None
        assert task.deleted_at is None

    def test_create_with_all_fields(self) -> None:
        due = date(2026, 3, 31)
        task = Task.create(
            title="重要タスク",
            priority=Priority.HIGH,
            due_date=due,
            category="仕事",
        )
        assert task.title == "重要タスク"
        assert task.priority == Priority.HIGH
        assert task.due_date == due
        assert task.category == "仕事"

    def test_to_dict(self) -> None:
        task = Task.create(title="タスク")
        d = task.to_dict()
        assert d["title"] == "タスク"
        assert d["done"] is False
        assert d["priority"] == "medium"
        assert d["due_date"] is None
        assert d["category"] is None
        assert d["deleted_at"] is None
        assert "id" in d
        assert "created_at" in d
        assert "updated_at" in d

    def test_from_dict_roundtrip(self) -> None:
        task = Task.create(
            title="往復テスト",
            priority=Priority.HIGH,
            due_date=date(2026, 4, 1),
            category="テスト",
        )
        d = task.to_dict()
        restored = Task.from_dict(d)
        assert restored.id == task.id
        assert restored.title == task.title
        assert restored.priority == task.priority
        assert restored.due_date == task.due_date
        assert restored.category == task.category
        assert restored.done == task.done
        assert restored.deleted_at == task.deleted_at
