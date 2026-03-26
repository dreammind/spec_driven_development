from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from todo_cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def tmp_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr("todo_cli.main._DATA_FILE", data_file)


class TestAddCommand:
    def test_add_basic(self) -> None:
        result = runner.invoke(app, ["add", "新しいタスク"])
        assert result.exit_code == 0
        assert "新しいタスク" in result.output

    def test_add_with_priority(self) -> None:
        result = runner.invoke(app, ["add", "重要タスク", "--priority", "high"])
        assert result.exit_code == 0

    def test_add_with_due_date(self) -> None:
        result = runner.invoke(app, ["add", "期限付き", "--due-date", "2026-04-01"])
        assert result.exit_code == 0

    def test_add_with_invalid_due_date(self) -> None:
        result = runner.invoke(app, ["add", "タスク", "--due-date", "invalid"])
        assert result.exit_code == 1

    def test_add_with_category(self) -> None:
        result = runner.invoke(app, ["add", "仕事タスク", "--category", "仕事"])
        assert result.exit_code == 0


class TestListCommand:
    def test_list_empty(self) -> None:
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "タスクがありません" in result.output

    def test_list_shows_tasks(self) -> None:
        runner.invoke(app, ["add", "タスク1"])
        runner.invoke(app, ["add", "タスク2"])
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "タスク1" in result.output
        assert "タスク2" in result.output

    def test_list_filter_undone(self) -> None:
        runner.invoke(app, ["add", "未完了"])
        result = runner.invoke(app, ["list", "--undone"])
        assert result.exit_code == 0

    def test_list_filter_done(self) -> None:
        result = runner.invoke(app, ["list", "--done"])
        assert result.exit_code == 0

    def test_list_filter_priority(self) -> None:
        result = runner.invoke(app, ["list", "--priority", "high"])
        assert result.exit_code == 0

    def test_list_filter_category(self) -> None:
        result = runner.invoke(app, ["list", "--category", "仕事"])
        assert result.exit_code == 0

    def test_list_filter_overdue(self) -> None:
        result = runner.invoke(app, ["list", "--overdue"])
        assert result.exit_code == 0

    def test_list_sort_priority(self) -> None:
        result = runner.invoke(app, ["list", "--sort", "priority"])
        assert result.exit_code == 0


class TestShowCommand:
    def test_show_existing_task(self) -> None:
        runner.invoke(app, ["add", "表示タスク"])
        list_result = runner.invoke(app, ["list"])
        task_id = list_result.output.split()[1] if list_result.output else ""

        from todo_cli.main import _DATA_FILE
        from todo_cli.repository import TaskRepository
        repo = TaskRepository(_DATA_FILE)
        tasks = repo.load()
        if tasks:
            result = runner.invoke(app, ["show", tasks[0].id])
            assert result.exit_code == 0
            assert "表示タスク" in result.output

    def test_show_nonexistent_task(self) -> None:
        result = runner.invoke(app, ["show", "nonexistent-id"])
        assert result.exit_code == 1


class TestDoneCommand:
    def test_complete_task(self) -> None:
        runner.invoke(app, ["add", "完了テスト"])
        from todo_cli.main import _DATA_FILE
        from todo_cli.repository import TaskRepository
        tasks = TaskRepository(_DATA_FILE).load()
        result = runner.invoke(app, ["done", tasks[0].id])
        assert result.exit_code == 0
        assert "完了" in result.output

    def test_complete_nonexistent_task(self) -> None:
        result = runner.invoke(app, ["done", "nonexistent-id"])
        assert result.exit_code == 1


class TestEditCommand:
    def test_edit_title(self) -> None:
        runner.invoke(app, ["add", "旧タイトル"])
        from todo_cli.main import _DATA_FILE
        from todo_cli.repository import TaskRepository
        tasks = TaskRepository(_DATA_FILE).load()
        result = runner.invoke(app, ["edit", tasks[0].id, "--title", "新タイトル"])
        assert result.exit_code == 0

    def test_edit_invalid_due_date(self) -> None:
        runner.invoke(app, ["add", "タスク"])
        from todo_cli.main import _DATA_FILE
        from todo_cli.repository import TaskRepository
        tasks = TaskRepository(_DATA_FILE).load()
        result = runner.invoke(app, ["edit", tasks[0].id, "--due-date", "bad-date"])
        assert result.exit_code == 1

    def test_edit_nonexistent_task(self) -> None:
        result = runner.invoke(app, ["edit", "nonexistent-id", "--title", "変更"])
        assert result.exit_code == 1


class TestDeleteCommand:
    def test_delete_task(self) -> None:
        runner.invoke(app, ["add", "削除タスク"])
        from todo_cli.main import _DATA_FILE
        from todo_cli.repository import TaskRepository
        tasks = TaskRepository(_DATA_FILE).load()
        result = runner.invoke(app, ["delete", tasks[0].id])
        assert result.exit_code == 0
        assert "削除" in result.output

    def test_delete_nonexistent_task(self) -> None:
        result = runner.invoke(app, ["delete", "nonexistent-id"])
        assert result.exit_code == 1


class TestSearchCommand:
    def test_search_found(self) -> None:
        runner.invoke(app, ["add", "レポートを提出する"])
        result = runner.invoke(app, ["search", "レポート"])
        assert result.exit_code == 0
        assert "レポート" in result.output

    def test_search_not_found(self) -> None:
        result = runner.invoke(app, ["search", "存在しないキーワード"])
        assert result.exit_code == 0
        assert "見つかりませんでした" in result.output
