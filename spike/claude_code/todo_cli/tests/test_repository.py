from datetime import date
from pathlib import Path

from todo_cli.models import Priority, Task
from todo_cli.repository import TaskRepository


class TestTaskRepository:
    def test_load_returns_empty_list_when_file_not_exists(self, tmp_path: Path) -> None:
        repo = TaskRepository(tmp_path / "tasks.json")
        assert repo.load() == []

    def test_save_and_load_single_task(self, tmp_path: Path) -> None:
        repo = TaskRepository(tmp_path / "tasks.json")
        task = Task.create(title="テストタスク")
        repo.save([task])
        loaded = repo.load()
        assert len(loaded) == 1
        assert loaded[0].id == task.id
        assert loaded[0].title == task.title

    def test_save_and_load_multiple_tasks(self, tmp_path: Path) -> None:
        repo = TaskRepository(tmp_path / "tasks.json")
        tasks = [
            Task.create(title="タスク1"),
            Task.create(title="タスク2", priority=Priority.HIGH),
            Task.create(title="タスク3", due_date=date(2026, 4, 1), category="仕事"),
        ]
        repo.save(tasks)
        loaded = repo.load()
        assert len(loaded) == 3
        assert loaded[0].title == "タスク1"
        assert loaded[1].priority == Priority.HIGH
        assert loaded[2].due_date == date(2026, 4, 1)
        assert loaded[2].category == "仕事"

    def test_overwrite_on_save(self, tmp_path: Path) -> None:
        repo = TaskRepository(tmp_path / "tasks.json")
        repo.save([Task.create(title="旧タスク")])
        repo.save([Task.create(title="新タスク")])
        loaded = repo.load()
        assert len(loaded) == 1
        assert loaded[0].title == "新タスク"

    def test_roundtrip_preserves_all_fields(self, tmp_path: Path) -> None:
        repo = TaskRepository(tmp_path / "tasks.json")
        task = Task.create(
            title="完全テスト",
            priority=Priority.LOW,
            due_date=date(2026, 12, 31),
            category="テスト",
        )
        repo.save([task])
        restored = repo.load()[0]
        assert restored.id == task.id
        assert restored.title == task.title
        assert restored.done == task.done
        assert restored.priority == task.priority
        assert restored.due_date == task.due_date
        assert restored.category == task.category
        assert restored.deleted_at == task.deleted_at
