from __future__ import annotations

from datetime import date

from rich.console import Console
from rich.table import Table

from todo_cli.models import Task

_DEFAULT_CONSOLE = Console()

_PRIORITY_LABEL = {"high": "高", "medium": "中", "low": "低"}


def print_task_list(tasks: list[Task], console: Console = _DEFAULT_CONSOLE) -> None:
    if not tasks:
        console.print("タスクがありません")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="dim", width=8)
    table.add_column("タイトル")
    table.add_column("優先度", width=6)
    table.add_column("期限", width=12)
    table.add_column("カテゴリ", width=10)
    table.add_column("状態", width=6)

    today = date.today()

    for task in tasks:
        due_str = ""
        if task.due_date:
            due_str = task.due_date.isoformat()
            if task.due_date < today:
                due_str += " [期限切れ]"

        status = "完了" if task.done else "未完了"
        priority_label = _PRIORITY_LABEL.get(task.priority.value, task.priority.value)

        table.add_row(
            task.id[:8],
            task.title,
            priority_label,
            due_str,
            task.category or "",
            status,
        )

    console.print(table)


def print_task_detail(task: Task, console: Console = _DEFAULT_CONSOLE) -> None:
    console.print(f"ID       : {task.id}")
    console.print(f"タイトル : {task.title}")
    console.print(f"優先度   : {task.priority.value}")
    console.print(f"期限     : {task.due_date.isoformat() if task.due_date else 'なし'}")
    console.print(f"カテゴリ : {task.category or 'なし'}")
    console.print(f"状態     : {'完了' if task.done else '未完了'}")
    console.print(f"作成日時 : {task.created_at.isoformat()}")
    console.print(f"更新日時 : {task.updated_at.isoformat()}")
