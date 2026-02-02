import json
from pathlib import Path
from typing import List
from datetime import date

import pytest
from src.todo.models import Task
from src.todo.database import load_tasks, save_tasks

@pytest.fixture
def sample_tasks() -> List[Task]:
    """Provides a list of sample Task objects."""
    return [
        Task(id=1, title="Buy groceries", priority=1, category="shopping", is_completed=False),
        Task(id=2, title="Read a book", priority=3, category="leisure", is_completed=True),
        Task(id=3, title="Call mom", priority=2, due_date=date(2026, 2, 5), category="family", is_completed=False),
    ]

def test_load_tasks_when_file_does_not_exist(tmp_path: Path):
    """
    Test that load_tasks returns an empty list if the tasks.json file does not exist.
    """
    db_path = tmp_path / "tasks.json"
    tasks = load_tasks(db_path)
    assert tasks == []

def test_load_tasks_when_file_is_empty(tmp_path: Path):
    """
    Test that load_tasks returns an empty list if the tasks.json file is empty.
    """
    db_path = tmp_path / "tasks.json"
    db_path.touch() # Create an empty file
    tasks = load_tasks(db_path)
    assert tasks == []

def test_load_tasks_with_valid_data(tmp_path: Path, sample_tasks: List[Task]):
    """
    Test that load_tasks correctly loads tasks from a valid tasks.json file.
    """
    db_path = tmp_path / "tasks.json"
    # Convert Pydantic models to JSON-compatible dictionaries
    tasks_data = [task.model_dump(mode='json') for task in sample_tasks]
    db_path.write_text(json.dumps(tasks_data))

    loaded_tasks = load_tasks(db_path)
    assert len(loaded_tasks) == len(sample_tasks)
    # Pydantic models can be compared directly if they have the same data
    assert loaded_tasks == sample_tasks

def test_save_tasks(tmp_path: Path, sample_tasks: List[Task]):
    """
    Test that save_tasks correctly writes a list of tasks to tasks.json.
    """
    db_path = tmp_path / "tasks.json"
    save_tasks(sample_tasks, db_path)

    assert db_path.exists()
    content = db_path.read_text()
    loaded_data = json.loads(content)
    
    # Compare loaded data with original sample tasks (converted to dicts)
    expected_data = [task.model_dump(mode='json') for task in sample_tasks]
    assert loaded_data == expected_data

def test_load_tasks_with_date_conversion(tmp_path: Path):
    """
    Test that load_tasks correctly converts date strings to date objects.
    """
    db_path = tmp_path / "tasks.json"
    task_data = {
        "id": 1,
        "title": "Task with date",
        "priority": 1,
        "due_date": "2026-03-01",
        "category": "work",
        "is_completed": False,
    }
    db_path.write_text(json.dumps([task_data]))

    loaded_tasks = load_tasks(db_path)
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == 1
    assert loaded_tasks[0].due_date == date(2026, 3, 1)

def test_load_tasks_with_none_date(tmp_path: Path):
    """
    Test that load_tasks correctly handles tasks with no due_date.
    """
    db_path = tmp_path / "tasks.json"
    task_data = {
        "id": 1,
        "title": "Task without date",
        "priority": 1,
        "due_date": None,
        "category": "work",
        "is_completed": False,
    }
    db_path.write_text(json.dumps([task_data]))

    loaded_tasks = load_tasks(db_path)
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == 1
    assert loaded_tasks[0].due_date is None

def test_load_tasks_with_malformed_json(tmp_path: Path, capsys):
    """
    Test that load_tasks returns an empty list and prints an error message
    if the tasks.json file contains malformed JSON.
    """
    db_path = tmp_path / "tasks.json"
    db_path.write_text("this is not json")
    
    tasks = load_tasks(db_path)
    assert tasks == []
    
    captured = capsys.readouterr()
    assert "Error loading tasks" in captured.out