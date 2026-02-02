import json
from datetime import date
from pathlib import Path
from typing import List, Optional
from unittest.mock import MagicMock, patch

import pytest
from src.todo.models import Task
from src.todo.manager import TaskManager  # This will be created later


@pytest.fixture
def mock_db_path() -> Path:
    """Fixture to provide a dummy database path."""
    return Path("dummy_tasks.json")

@pytest.fixture
def sample_tasks_data() -> List[dict]:
    """Provides sample task data in dictionary format."""
    return [
        {"id": 1, "title": "Buy groceries", "priority": 1, "due_date": None, "category": "shopping", "is_completed": False},
        {"id": 2, "title": "Read a book", "priority": 3, "due_date": None, "category": "leisure", "is_completed": True},
        {"id": 3, "title": "Call mom", "priority": 2, "due_date": "2026-02-05", "category": "family", "is_completed": False},
    ]

@pytest.fixture
def mock_load_tasks(sample_tasks_data: List[dict]):
    """Mocks the database.load_tasks function."""
    # Patch load_tasks where TaskManager imports it from
    with patch('src.todo.manager.load_tasks') as mock: # Changed patch target
        mock.return_value = [Task.model_validate(data) for data in sample_tasks_data]
        yield mock

@pytest.fixture
def mock_save_tasks():
    """Mocks the database.save_tasks function."""
    # Patch save_tasks where TaskManager imports it from
    with patch('src.todo.manager.save_tasks') as mock: # Changed patch target
        yield mock

@pytest.fixture
def task_manager(mock_load_tasks, mock_save_tasks, mock_db_path) -> TaskManager:
    """Provides an initialized TaskManager instance."""
    return TaskManager(db_path=mock_db_path)


def test_task_manager_initialization(mock_load_tasks, task_manager):
    """Test that TaskManager loads tasks on initialization."""
    mock_load_tasks.assert_called_once()
    assert len(task_manager._tasks) == 3


def test_get_next_id(task_manager):
    """Test that get_next_id returns the correct next ID."""
    assert task_manager.get_next_id() == 4
    # Add a task and check again
    task_manager.add_task("New task", 1)
    assert task_manager.get_next_id() == 5


def test_add_task(task_manager, mock_save_tasks):
    """Test adding a new task."""
    new_task = task_manager.add_task("Walk the dog", priority=1, category="chores")
    assert isinstance(new_task, Task)
    assert new_task.title == "Walk the dog"
    assert new_task.priority == 1
    assert new_task.category == "chores"
    assert not new_task.is_completed
    assert len(task_manager._tasks) == 4  # 3 initial + 1 new
    mock_save_tasks.assert_called_once()


def test_list_tasks(task_manager):
    """Test listing tasks without filters."""
    tasks = task_manager.list_tasks()
    assert len(tasks) == 3
    assert tasks[0].title == "Buy groceries"


def test_list_tasks_by_category(task_manager):
    """Test listing tasks filtered by category."""
    shopping_tasks = task_manager.list_tasks(category="shopping")
    assert len(shopping_tasks) == 1
    assert shopping_tasks[0].title == "Buy groceries"

    non_existent_category_tasks = task_manager.list_tasks(category="nonexistent")
    assert len(non_existent_category_tasks) == 0


def test_list_tasks_sorted_by_priority(task_manager):
    """Test listing tasks sorted by priority (ascending)."""
    # default sort order is priority ascending, then id ascending
    tasks = task_manager.list_tasks(sort_by="priority")
    assert tasks[0].title == "Buy groceries"  # priority 1
    assert tasks[1].title == "Call mom"       # priority 2
    assert tasks[2].title == "Read a book"    # priority 3

def test_list_tasks_sorted_by_due_date(task_manager):
    """Test listing tasks sorted by due date."""
    # Assuming sample_tasks_data:
    # id=1, due_date=None
    # id=2, due_date=None
    # id=3, due_date="2026-02-05"
    # Expected sort: id=3 (due_date first), then id=1, id=2 (None due_dates last, then by ID)
    tasks = task_manager.list_tasks(sort_by="due-date")
    assert tasks[0].id == 3 # Has a due_date
    assert tasks[1].id == 1 # None due_date, earlier ID
    assert tasks[2].id == 2 # None due_date, later ID


def test_list_tasks_default_sort(task_manager):
    """Test listing tasks with default sort (by ID)."""
    tasks = task_manager.list_tasks() # Should implicitly sort by ID if no sort_by is given
    assert tasks[0].id == 1
    assert tasks[1].id == 2
    assert tasks[2].id == 3

def test_list_tasks_invalid_sort_by(task_manager):
    """Test listing tasks with an invalid sort_by value, should default to ID sort."""
    tasks = task_manager.list_tasks(sort_by="invalid_sort")
    assert tasks[0].id == 1
    assert tasks[1].id == 2
    assert tasks[2].id == 3


def test_delete_task_success(task_manager, mock_save_tasks):
    """Test deleting an existing task."""
    result = task_manager.delete_task(1)
    assert result is True
    assert len(task_manager._tasks) == 2
    assert task_manager.get_task_by_id(1) is None
    mock_save_tasks.assert_called_once()


def test_delete_task_not_found(task_manager, mock_save_tasks):
    """Test deleting a non-existent task."""
    result = task_manager.delete_task(999)
    assert result is False
    assert len(task_manager._tasks) == 3  # No change
    mock_save_tasks.assert_not_called()


def test_edit_task_success(task_manager, mock_save_tasks):
    """Test editing an existing task."""
    edited_task = task_manager.edit_task(1, title="Buy organic groceries", priority=1, category="organic shopping")
    assert edited_task is not None
    assert edited_task.id == 1
    assert edited_task.title == "Buy organic groceries"
    assert edited_task.category == "organic shopping"
    mock_save_tasks.assert_called_once()

def test_edit_task_success_with_due_date(task_manager, mock_save_tasks):
    """Test editing an existing task including its due_date."""
    edited_task = task_manager.edit_task(3, due_date=date(2026, 3, 10)) # Edit task with ID 3
    assert edited_task is not None
    assert edited_task.id == 3
    assert edited_task.due_date == date(2026, 3, 10)
    mock_save_tasks.assert_called_once()


def test_edit_task_not_found(task_manager, mock_save_tasks):
    """Test editing a non-existent task."""
    edited_task = task_manager.edit_task(999, title="Non-existent task")
    assert edited_task is None
    mock_save_tasks.assert_not_called()


def test_complete_task_success(task_manager, mock_save_tasks):
    """Test completing an existing task."""
    completed_task = task_manager.complete_task(1)
    assert completed_task is not None
    assert completed_task.id == 1
    assert completed_task.is_completed is True
    mock_save_tasks.assert_called_once()


def test_complete_task_not_found(task_manager, mock_save_tasks):
    """Test completing a non-existent task."""
    completed_task = task_manager.complete_task(999)
    assert completed_task is None
    mock_save_tasks.assert_not_called()


def test_search_tasks_by_keyword(task_manager):
    """Test searching tasks by keyword in title."""
    search_results = task_manager.search_tasks(keyword="book")
    assert len(search_results) == 1
    assert search_results[0].title == "Read a book"

    search_results = task_manager.search_tasks(keyword="Buy")
    assert len(search_results) == 1
    assert search_results[0].title == "Buy groceries"

    no_results = task_manager.search_tasks(keyword="xyz")
    assert len(no_results) == 0
