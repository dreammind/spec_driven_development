from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import ValidationError

from todo_cli.models import Task, TaskCollection


class TaskRepositoryError(Exception):
    pass


class InvalidTaskIdError(TaskRepositoryError):
    pass


class TaskNotFoundError(TaskRepositoryError):
    pass


class TaskAlreadyArchivedError(TaskRepositoryError):
    pass


class TaskNotArchivedError(TaskRepositoryError):
    pass


class TaskEditArchivedError(TaskRepositoryError):
    pass


class TaskValidationError(TaskRepositoryError):
    pass


class TaskRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path

    def _ensure_parent_dir(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load_collection(self) -> TaskCollection:
        if not self.storage_path.exists():
            return TaskCollection()

        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        try:
            return TaskCollection.model_validate(data)
        except ValidationError as exc:
            raise TaskValidationError(str(exc)) from exc

    def save_collection(self, collection: TaskCollection) -> None:
        self._ensure_parent_dir()
        payload = collection.model_dump(mode="json")
        self.storage_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _parse_id(self, task_id: str) -> UUID:
        try:
            return UUID(task_id)
        except ValueError as exc:
            raise InvalidTaskIdError(f"invalid task id: {task_id}") from exc

    def _find_index(self, tasks: list[Task], task_id: UUID) -> int:
        for i, task in enumerate(tasks):
            if task.id == task_id:
                return i
        raise TaskNotFoundError(f"task not found: {task_id}")

    def add_task(self, title: str) -> Task:
        collection = self.load_collection()
        try:
            task = Task(id=uuid4(), title=title)
        except ValidationError as exc:
            raise TaskValidationError(str(exc)) from exc

        collection.tasks.append(task)
        self.save_collection(collection)
        return task

    def list_tasks(self, include_completed: bool = False) -> list[Task]:
        collection = self.load_collection()
        tasks = [task for task in collection.tasks if not task.is_archived]
        if not include_completed:
            tasks = [task for task in tasks if not task.is_completed]
        return tasks

    def complete_task(self, task_id: str) -> Task:
        parsed_id = self._parse_id(task_id)
        collection = self.load_collection()
        idx = self._find_index(collection.tasks, parsed_id)
        collection.tasks[idx] = collection.tasks[idx].complete()
        self.save_collection(collection)
        return collection.tasks[idx]

    def reopen_task(self, task_id: str) -> Task:
        parsed_id = self._parse_id(task_id)
        collection = self.load_collection()
        idx = self._find_index(collection.tasks, parsed_id)
        collection.tasks[idx] = collection.tasks[idx].reopen()
        self.save_collection(collection)
        return collection.tasks[idx]

    def archive_task(self, task_id: str) -> Task:
        parsed_id = self._parse_id(task_id)
        collection = self.load_collection()
        idx = self._find_index(collection.tasks, parsed_id)

        if collection.tasks[idx].is_archived:
            raise TaskAlreadyArchivedError(f"task already archived: {parsed_id}")

        collection.tasks[idx] = collection.tasks[idx].archive()
        self.save_collection(collection)
        return collection.tasks[idx]

    def restore_task(self, task_id: str) -> Task:
        parsed_id = self._parse_id(task_id)
        collection = self.load_collection()
        idx = self._find_index(collection.tasks, parsed_id)

        if not collection.tasks[idx].is_archived:
            raise TaskNotArchivedError(f"task is not archived: {parsed_id}")

        collection.tasks[idx] = collection.tasks[idx].restore()
        self.save_collection(collection)
        return collection.tasks[idx]

    def edit_task_title(self, task_id: str, new_title: str) -> Task:
        parsed_id = self._parse_id(task_id)
        collection = self.load_collection()
        idx = self._find_index(collection.tasks, parsed_id)
        task = collection.tasks[idx]

        if task.is_archived:
            raise TaskEditArchivedError(
                f"task is archived; restore before editing: {parsed_id}"
            )

        try:
            normalized_title = Task.normalize_title(new_title)
        except ValueError as exc:
            raise TaskValidationError(str(exc)) from exc

        collection.tasks[idx] = task.model_copy(update={"title": normalized_title})
        self.save_collection(collection)
        return collection.tasks[idx]
