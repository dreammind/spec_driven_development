from datetime import date
from pathlib import Path
from typing import List, Optional, Any
from operator import attrgetter

from src.todo.models import Task
from src.todo.database import load_tasks, save_tasks


class TaskManager:
    def __init__(self, db_path: Path = Path("tasks.json")):
        self.db_path = db_path
        self._tasks: List[Task] = load_tasks(self.db_path)

    def _save(self):
        """Internal method to save the current state of tasks to the database."""
        save_tasks(self._tasks, self.db_path)

    def get_next_id(self) -> int:
        """Generates the next available ID for a new task."""
        return max((task.id for task in self._tasks), default=0) + 1

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Helper method to find a task by its ID."""
        return next((task for task in self._tasks if task.id == task_id), None)

    def add_task(self, title: str, priority: int = 3, due_date: Optional[date] = None, category: str = "default") -> Task:
        """Adds a new task to the list and saves it."""
        new_id = self.get_next_id()
        new_task = Task(
            id=new_id,
            title=title,
            priority=priority,
            due_date=due_date,
            category=category,
            is_completed=False
        )
        self._tasks.append(new_task)
        self._save()
        return new_task

    def edit_task(self, task_id: int, title: Optional[str] = None, priority: Optional[int] = None, due_date: Optional[date] = None, category: Optional[str] = None) -> Optional[Task]:
        """Edits an existing task and saves the changes."""
        task_to_edit = self.get_task_by_id(task_id)
        if task_to_edit:
            if title is not None:
                task_to_edit.title = title
            if priority is not None:
                task_to_edit.priority = priority
            if due_date is not None:
                task_to_edit.due_date = due_date
            if category is not None:
                task_to_edit.category = category
            self._save()
            return task_to_edit
        return None

    def delete_task(self, task_id: int) -> bool:
        """Deletes a task by ID and saves the changes."""
        initial_len = len(self._tasks)
        self._tasks = [task for task in self._tasks if task.id != task_id]
        if len(self._tasks) < initial_len:
            self._save()
            return True
        return False

    def complete_task(self, task_id: int) -> Optional[Task]:
        """Marks a task as completed and saves the changes."""
        task_to_complete = self.get_task_by_id(task_id)
        if task_to_complete:
            task_to_complete.is_completed = True
            self._save()
            return task_to_complete
        return None

    def list_tasks(self, category: Optional[str] = None, sort_by: Optional[str] = None) -> List[Task]:
        """
        Lists tasks, optionally filtered by category and sorted by priority or due date.
        """
        filtered_tasks = self._tasks
        if category:
            filtered_tasks = [task for task in filtered_tasks if task.category == category]

        if sort_by == "priority":
            # Sort by priority ascending, then by ID ascending for stable sort
            filtered_tasks.sort(key=attrgetter('priority', 'id'))
        elif sort_by == "due-date":
            # Sort by due_date (None values last), then by ID ascending
            # Use a tuple for sorting: (is_due_date_none, due_date_value, id)
            # This ensures None due_dates are always at the end
            filtered_tasks.sort(key=lambda task: (task.due_date is None, task.due_date, task.id))
        else:
            # Default sort by ID
            filtered_tasks.sort(key=attrgetter('id'))

        return filtered_tasks

    def search_tasks(self, keyword: str) -> List[Task]:
        """Searches tasks by keyword in their title."""
        keyword_lower = keyword.lower()
        return [task for task in self._tasks if keyword_lower in task.title.lower()]