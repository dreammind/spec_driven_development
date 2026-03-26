from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from todo_cli.models import Priority, Task
from todo_cli.repository import TaskRepository


class TaskNotFoundError(Exception):
    pass


class SortKey(str, Enum):
    PRIORITY = "priority"
    DUE_DATE = "due-date"
    CREATED_AT = "created-at"


_PRIORITY_ORDER = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def add_task(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
        category: str | None = None,
    ) -> Task:
        tasks = self._repo.load()
        task = Task.create(title=title, priority=priority, due_date=due_date, category=category)
        tasks.append(task)
        self._repo.save(tasks)
        return task

    def list_tasks(
        self,
        done: bool | None = None,
        priority: Priority | None = None,
        category: str | None = None,
        overdue: bool = False,
        sort: SortKey | None = None,
    ) -> list[Task]:
        tasks = [t for t in self._repo.load() if t.deleted_at is None]

        if done is not None:
            tasks = [t for t in tasks if t.done == done]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        if category is not None:
            tasks = [t for t in tasks if t.category == category]
        if overdue:
            today = date.today()
            tasks = [t for t in tasks if t.due_date is not None and t.due_date < today]

        if sort == SortKey.PRIORITY:
            tasks.sort(key=lambda t: _PRIORITY_ORDER[t.priority])
        elif sort == SortKey.DUE_DATE:
            tasks.sort(key=lambda t: (t.due_date is None, t.due_date))
        elif sort == SortKey.CREATED_AT:
            tasks.sort(key=lambda t: t.created_at)

        return tasks

    def get_task(self, task_id: str) -> Task | None:
        for task in self._repo.load():
            if task.id == task_id and task.deleted_at is None:
                return task
        return None

    def complete_task(self, task_id: str) -> Task:
        tasks = self._repo.load()
        for task in tasks:
            if task.id == task_id and task.deleted_at is None:
                task.done = True
                task.updated_at = datetime.now()
                self._repo.save(tasks)
                return task
        raise TaskNotFoundError(f"タスクID \"{task_id}\" が見つかりません")

    def edit_task(
        self,
        task_id: str,
        title: str | None = None,
        priority: Priority | None = None,
        due_date: date | None = None,
        category: str | None = None,
    ) -> Task:
        tasks = self._repo.load()
        for task in tasks:
            if task.id == task_id and task.deleted_at is None:
                if title is not None:
                    task.title = title
                if priority is not None:
                    task.priority = priority
                if due_date is not None:
                    task.due_date = due_date
                if category is not None:
                    task.category = category
                task.updated_at = datetime.now()
                self._repo.save(tasks)
                return task
        raise TaskNotFoundError(f"タスクID \"{task_id}\" が見つかりません")

    def delete_task(self, task_id: str) -> Task:
        tasks = self._repo.load()
        for task in tasks:
            if task.id == task_id and task.deleted_at is None:
                task.deleted_at = datetime.now()
                task.updated_at = datetime.now()
                self._repo.save(tasks)
                return task
        raise TaskNotFoundError(f"タスクID \"{task_id}\" が見つかりません")

    def search_tasks(self, keyword: str) -> list[Task]:
        return [
            t for t in self._repo.load()
            if t.deleted_at is None and keyword.lower() in t.title.lower()
        ]
