from datetime import date, timedelta
from io import StringIO

import pytest
from rich.console import Console

from todo_cli.display import print_task_detail, print_task_list
from todo_cli.models import Priority, Task


def capture_output(func: object, *args: object) -> str:
    buf = StringIO()
    console = Console(file=buf, highlight=False, no_color=True)
    import inspect
    if callable(func):
        sig = inspect.signature(func)  # type: ignore[arg-type]
        params = list(sig.parameters.keys())
        if "console" in params:
            func(*args, console=console)  # type: ignore[operator]
        else:
            func(*args)  # type: ignore[operator]
    return buf.getvalue()


class TestPrintTaskList:
    def test_empty_list_shows_message(self) -> None:
        buf = StringIO()
        console = Console(file=buf, highlight=False, no_color=True)
        print_task_list([], console=console)
        assert "タスクがありません" in buf.getvalue()

    def test_task_titles_are_shown(self) -> None:
        buf = StringIO()
        console = Console(file=buf, highlight=False, no_color=True)
        tasks = [Task.create(title="テストタスク1"), Task.create(title="テストタスク2")]
        print_task_list(tasks, console=console)
        output = buf.getvalue()
        assert "テストタスク1" in output
        assert "テストタスク2" in output

    def test_overdue_task_is_marked(self) -> None:
        buf = StringIO()
        console = Console(file=buf, highlight=False, no_color=True)
        past = date.today() - timedelta(days=1)
        task = Task.create(title="期限切れタスク", due_date=past)
        print_task_list([task], console=console)
        output = buf.getvalue()
        assert "期限切れ" in output or "OVERDUE" in output.upper() or past.isoformat() in output

    def test_priority_is_shown(self) -> None:
        buf = StringIO()
        console = Console(file=buf, highlight=False, no_color=True)
        task = Task.create(title="高優先度", priority=Priority.HIGH)
        print_task_list([task], console=console)
        output = buf.getvalue()
        assert "high" in output.lower() or "高" in output


class TestPrintTaskDetail:
    def test_all_fields_shown(self) -> None:
        buf = StringIO()
        console = Console(file=buf, highlight=False, no_color=True)
        task = Task.create(
            title="詳細テスト",
            priority=Priority.HIGH,
            due_date=date(2026, 4, 1),
            category="仕事",
        )
        print_task_detail(task, console=console)
        output = buf.getvalue()
        assert "詳細テスト" in output
        assert "high" in output.lower() or "高" in output
        assert "2026-04-01" in output
        assert "仕事" in output
