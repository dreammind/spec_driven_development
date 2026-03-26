from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from todo_cli.models import Priority, Task
from todo_cli.repository import TaskRepository
from todo_cli.service import SortKey, TaskNotFoundError, TaskService


@pytest.fixture
def service(tmp_path: Path) -> TaskService:
    repo = TaskRepository(tmp_path / "tasks.json")
    return TaskService(repo)


class TestAddTask:
    def test_add_basic_task(self, service: TaskService) -> None:
        task = service.add_task("新しいタスク")
        assert task.title == "新しいタスク"
        assert task.done is False
        assert task.priority == Priority.MEDIUM
        assert task.id != ""
        assert isinstance(task.created_at, datetime)

    def test_add_task_with_all_options(self, service: TaskService) -> None:
        due = date(2026, 4, 1)
        task = service.add_task("詳細タスク", priority=Priority.HIGH, due_date=due, category="仕事")
        assert task.priority == Priority.HIGH
        assert task.due_date == due
        assert task.category == "仕事"

    def test_added_task_is_persisted(self, service: TaskService) -> None:
        service.add_task("永続化テスト")
        tasks = service.list_tasks()
        assert len(tasks) == 1


class TestListTasks:
    def test_list_excludes_deleted(self, service: TaskService) -> None:
        t1 = service.add_task("残すタスク")
        t2 = service.add_task("削除タスク")
        service.delete_task(t2.id)
        tasks = service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == t1.id

    def test_filter_done(self, service: TaskService) -> None:
        t1 = service.add_task("未完了")
        t2 = service.add_task("完了済み")
        service.complete_task(t2.id)
        assert len(service.list_tasks(done=True)) == 1
        assert len(service.list_tasks(done=False)) == 1

    def test_filter_priority(self, service: TaskService) -> None:
        service.add_task("高", priority=Priority.HIGH)
        service.add_task("低", priority=Priority.LOW)
        result = service.list_tasks(priority=Priority.HIGH)
        assert len(result) == 1
        assert result[0].priority == Priority.HIGH

    def test_filter_category(self, service: TaskService) -> None:
        service.add_task("仕事タスク", category="仕事")
        service.add_task("趣味タスク", category="趣味")
        result = service.list_tasks(category="仕事")
        assert len(result) == 1
        assert result[0].category == "仕事"

    def test_filter_overdue(self, service: TaskService) -> None:
        past = date.today() - timedelta(days=1)
        future = date.today() + timedelta(days=1)
        service.add_task("期限切れ", due_date=past)
        service.add_task("期限内", due_date=future)
        result = service.list_tasks(overdue=True)
        assert len(result) == 1
        assert result[0].title == "期限切れ"

    def test_sort_by_priority(self, service: TaskService) -> None:
        service.add_task("低", priority=Priority.LOW)
        service.add_task("高", priority=Priority.HIGH)
        service.add_task("中", priority=Priority.MEDIUM)
        result = service.list_tasks(sort=SortKey.PRIORITY)
        assert result[0].priority == Priority.HIGH
        assert result[2].priority == Priority.LOW

    def test_sort_by_due_date(self, service: TaskService) -> None:
        service.add_task("遅い", due_date=date(2026, 12, 31))
        service.add_task("期限なし")
        service.add_task("早い", due_date=date(2026, 1, 1))
        result = service.list_tasks(sort=SortKey.DUE_DATE)
        assert result[0].due_date == date(2026, 1, 1)

    def test_sort_by_created_at(self, service: TaskService) -> None:
        t1 = service.add_task("最初")
        t2 = service.add_task("次")
        result = service.list_tasks(sort=SortKey.CREATED_AT)
        assert result[0].id == t1.id
        assert result[1].id == t2.id


class TestGetTask:
    def test_get_existing_task(self, service: TaskService) -> None:
        task = service.add_task("取得テスト")
        found = service.get_task(task.id)
        assert found is not None
        assert found.id == task.id

    def test_get_nonexistent_task_returns_none(self, service: TaskService) -> None:
        assert service.get_task("nonexistent-id") is None


class TestCompleteTask:
    def test_complete_task(self, service: TaskService) -> None:
        task = service.add_task("完了テスト")
        updated = service.complete_task(task.id)
        assert updated.done is True
        assert updated.updated_at >= task.updated_at

    def test_complete_nonexistent_task_raises(self, service: TaskService) -> None:
        with pytest.raises(TaskNotFoundError):
            service.complete_task("nonexistent-id")


class TestEditTask:
    def test_edit_title(self, service: TaskService) -> None:
        task = service.add_task("旧タイトル")
        updated = service.edit_task(task.id, title="新タイトル")
        assert updated.title == "新タイトル"

    def test_edit_priority(self, service: TaskService) -> None:
        task = service.add_task("タスク")
        updated = service.edit_task(task.id, priority=Priority.LOW)
        assert updated.priority == Priority.LOW

    def test_edit_due_date(self, service: TaskService) -> None:
        task = service.add_task("タスク")
        new_due = date(2026, 6, 1)
        updated = service.edit_task(task.id, due_date=new_due)
        assert updated.due_date == new_due

    def test_edit_category(self, service: TaskService) -> None:
        task = service.add_task("タスク")
        updated = service.edit_task(task.id, category="新カテゴリ")
        assert updated.category == "新カテゴリ"

    def test_edit_updates_updated_at(self, service: TaskService) -> None:
        task = service.add_task("タスク")
        updated = service.edit_task(task.id, title="変更")
        assert updated.updated_at >= task.updated_at

    def test_edit_nonexistent_task_raises(self, service: TaskService) -> None:
        with pytest.raises(TaskNotFoundError):
            service.edit_task("nonexistent-id", title="変更")


class TestDeleteTask:
    def test_delete_sets_deleted_at(self, service: TaskService) -> None:
        task = service.add_task("削除テスト")
        deleted = service.delete_task(task.id)
        assert deleted.deleted_at is not None

    def test_deleted_task_not_in_list(self, service: TaskService) -> None:
        task = service.add_task("削除されるタスク")
        service.delete_task(task.id)
        assert service.list_tasks() == []

    def test_delete_nonexistent_task_raises(self, service: TaskService) -> None:
        with pytest.raises(TaskNotFoundError):
            service.delete_task("nonexistent-id")


class TestSearchTasks:
    def test_search_by_keyword(self, service: TaskService) -> None:
        service.add_task("レポートを提出する")
        service.add_task("買い物をする")
        result = service.search_tasks("レポート")
        assert len(result) == 1
        assert result[0].title == "レポートを提出する"

    def test_search_partial_match(self, service: TaskService) -> None:
        service.add_task("プロジェクト計画を立てる")
        result = service.search_tasks("計画")
        assert len(result) == 1

    def test_search_no_match_returns_empty(self, service: TaskService) -> None:
        service.add_task("タスク")
        assert service.search_tasks("存在しない") == []

    def test_search_excludes_deleted(self, service: TaskService) -> None:
        task = service.add_task("削除済みタスク")
        service.delete_task(task.id)
        assert service.search_tasks("削除済み") == []
