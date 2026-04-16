from __future__ import annotations

from pathlib import Path

from todo_cli.models import Task
from todo_cli.repository import TaskRepository


class TodoApp:
    def __init__(self, storage_path: Path) -> None:
        self.repo = TaskRepository(storage_path=storage_path)

    def add_task(self, title: str) -> Task:
        return self.repo.add_task(title=title)

    def list_tasks(self, include_completed: bool = False) -> list[Task]:
        return self.repo.list_tasks(include_completed=include_completed)

    def complete_task(self, task_id: str) -> Task:
        return self.repo.complete_task(task_id=task_id)

    def reopen_task(self, task_id: str) -> Task:
        return self.repo.reopen_task(task_id=task_id)

    def archive_task(self, task_id: str) -> Task:
        return self.repo.archive_task(task_id=task_id)

    def restore_task(self, task_id: str) -> Task:
        return self.repo.restore_task(task_id=task_id)
