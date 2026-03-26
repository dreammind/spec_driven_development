from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import typer

from todo_cli.display import print_task_detail, print_task_list
from todo_cli.models import Priority
from todo_cli.repository import TaskRepository
from todo_cli.service import SortKey, TaskNotFoundError, TaskService

app = typer.Typer(help="CLIタスク管理アプリ")

_DATA_FILE = Path.home() / ".todo_cli" / "tasks.json"


def _get_service() -> TaskService:
    return TaskService(TaskRepository(_DATA_FILE))


@app.command()
def add(
    title: str = typer.Argument(..., help="タスクのタイトル"),
    priority: Priority = typer.Option(Priority.MEDIUM, "--priority", "-p", help="優先度 (high/medium/low)"),
    due_date: Optional[str] = typer.Option(None, "--due-date", "-d", help="期限 (YYYY-MM-DD)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="カテゴリ"),
) -> None:
    """タスクを追加する"""
    parsed_due: date | None = None
    if due_date:
        try:
            parsed_due = date.fromisoformat(due_date)
        except ValueError:
            typer.echo("Error: 日付は YYYY-MM-DD 形式で入力してください", err=True)
            raise typer.Exit(1)

    service = _get_service()
    task = service.add_task(title, priority=priority, due_date=parsed_due, category=category)
    typer.echo(f"タスクを追加しました: [{task.id[:8]}] {task.title}")


@app.command(name="list")
def list_tasks(
    done: Optional[bool] = typer.Option(None, "--done/--undone", help="完了/未完了で絞り込む"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p", help="優先度で絞り込む"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="カテゴリで絞り込む"),
    overdue: bool = typer.Option(False, "--overdue", help="期限切れのみ表示"),
    sort: Optional[SortKey] = typer.Option(None, "--sort", "-s", help="並べ替え (priority/due-date/created-at)"),
) -> None:
    """タスク一覧を表示する"""
    service = _get_service()
    tasks = service.list_tasks(done=done, priority=priority, category=category, overdue=overdue, sort=sort)
    print_task_list(tasks)


@app.command()
def show(
    task_id: str = typer.Argument(..., help="タスクID"),
) -> None:
    """タスクの詳細を表示する"""
    service = _get_service()
    task = service.get_task(task_id)
    if task is None:
        typer.echo(f"Error: タスクID \"{task_id}\" が見つかりません", err=True)
        raise typer.Exit(1)
    print_task_detail(task)


@app.command()
def done(
    task_id: str = typer.Argument(..., help="タスクID"),
) -> None:
    """タスクを完了にする"""
    service = _get_service()
    try:
        task = service.complete_task(task_id)
        typer.echo(f"完了にしました: [{task.id[:8]}] {task.title}")
    except TaskNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def edit(
    task_id: str = typer.Argument(..., help="タスクID"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="新しいタイトル"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p", help="新しい優先度"),
    due_date: Optional[str] = typer.Option(None, "--due-date", "-d", help="新しい期限 (YYYY-MM-DD)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="新しいカテゴリ"),
) -> None:
    """タスクを編集する"""
    parsed_due: date | None = None
    if due_date:
        try:
            parsed_due = date.fromisoformat(due_date)
        except ValueError:
            typer.echo("Error: 日付は YYYY-MM-DD 形式で入力してください", err=True)
            raise typer.Exit(1)

    service = _get_service()
    try:
        task = service.edit_task(task_id, title=title, priority=priority, due_date=parsed_due, category=category)
        typer.echo(f"更新しました: [{task.id[:8]}] {task.title}")
    except TaskNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def delete(
    task_id: str = typer.Argument(..., help="タスクID"),
) -> None:
    """タスクを削除する"""
    service = _get_service()
    try:
        task = service.delete_task(task_id)
        typer.echo(f"削除しました: [{task.id[:8]}] {task.title}")
    except TaskNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def search(
    keyword: str = typer.Argument(..., help="検索キーワード"),
) -> None:
    """タイトルをキーワードで検索する"""
    service = _get_service()
    tasks = service.search_tasks(keyword)
    if not tasks:
        typer.echo("該当するタスクが見つかりませんでした")
        return
    print_task_list(tasks)
