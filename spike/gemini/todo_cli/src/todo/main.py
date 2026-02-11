import typer
from typing import Optional
from datetime import datetime, date

from todo.manager import TaskManager
from todo.models import Task

app = typer.Typer(help="A simple command-line TODO application.")
task_manager = TaskManager() # Initialize TaskManager

# Helper function to print task details
def _print_task(task: Task):
    status = "✅" if task.is_completed else "⏳"
    due_date_str = task.due_date.isoformat() if task.due_date else "N/A"
    typer.echo(
        f"{status} ID: {task.id} | Title: {task.title} | Priority: {task.priority} | Due: {due_date_str} | Category: {task.category}"
    )

@app.command()
def add(
    title: str = typer.Argument(..., help="The title of the task."),
    priority: int = typer.Option(3, "--priority", "-p", min=1, max=5, help="Priority from 1 (high) to 5 (low)."),
    due_date: Optional[datetime] = typer.Option(
        None, "--due-date", "-d", formats=["%Y-%m-%d"],
        help="Due date in YYYY-MM-DD format."
    ),
    category: str = typer.Option("default", "--category", "-c", help="Category of the task."),
):
    """Adds a new TODO task."""
    due_date_obj = due_date.date() if due_date else None
    new_task = task_manager.add_task(
        title=title,
        priority=priority,
        due_date=due_date_obj,
        category=category,
    )
    typer.echo(f"Task added: {new_task.title} (ID: {new_task.id})")

@app.command()
def list(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter tasks by category."),
    sort_by: Optional[str] = typer.Option(None, "--sort-by", "-s", help="Sort tasks by 'priority' or 'due-date'."),
):
    """Lists all TODO tasks."""
    tasks = task_manager.list_tasks(category=category, sort_by=sort_by)
    if not tasks:
        typer.echo("No tasks found.")
        return

    typer.echo("\n--- Your TODOs ---")
    for task in tasks:
        _print_task(task)
    typer.echo("------------------\n")

@app.command()
def edit(
    task_id: int = typer.Argument(..., help="The ID of the task to edit."),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title for the task."),
    priority: Optional[int] = typer.Option(None, "--priority", "-p", min=1, max=5, help="New priority for the task."),
    due_date: Optional[datetime] = typer.Option(
        None, "--due-date", "-d", formats=["%Y-%m-%d"],
        help="New due date in YYYY-MM-DD format."
    ),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="New category for the task."),
):
    """Edits an existing TODO task."""
    due_date_obj = due_date.date() if due_date else None
    updated_task = task_manager.edit_task(
        task_id=task_id,
        title=title,
        priority=priority,
        due_date=due_date_obj,
        category=category,
    )
    if updated_task:
        typer.echo(f"Task ID {task_id} updated:")
        _print_task(updated_task)
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.")

@app.command()
def complete(
    task_id: int = typer.Argument(..., help="The ID of the task to mark as complete."),
):
    """Marks a TODO task as complete."""
    completed_task = task_manager.complete_task(task_id)
    if completed_task:
        typer.echo(f"Task ID {task_id} marked as complete:")
        _print_task(completed_task)
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.")

@app.command()
def delete(
    task_id: int = typer.Argument(..., help="The ID of the task to delete."),
):
    """Deletes a TODO task."""
    if task_manager.delete_task(task_id):
        typer.echo(f"Task ID {task_id} deleted successfully.")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.")

@app.command()
def search(
    keyword: str = typer.Argument(..., help="Keyword to search in task titles."),
):
    """Searches TODO tasks by keyword."""
    results = task_manager.search_tasks(keyword)
    if not results:
        typer.echo(f"No tasks found matching '{keyword}'.")
        return
    
    typer.echo(f"\n--- Search results for '{keyword}' ---")
    for task in results:
        _print_task(task)
    typer.echo("------------------------------------\n")

if __name__ == "__main__":
    app()
