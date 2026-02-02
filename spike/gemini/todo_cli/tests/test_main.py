import json
from pathlib import Path
from typer.testing import CliRunner

import pytest
from src.todo.main import app, task_manager # Import app and the initialized task_manager
from src.todo.models import Task

runner = CliRunner()

@pytest.fixture(autouse=True)
def setup_teardown_db(tmp_path):
    """
    Fixture to create a clean tasks.json for each test and remove it afterwards.
    Also, ensure the TaskManager in main.py uses this temporary path.
    """
    test_db_path = tmp_path / "tasks.json"
    # Overwrite the TaskManager's db_path for the test
    task_manager.db_path = test_db_path
    task_manager._tasks = [] # Ensure it starts clean for the test
    yield
    # Cleanup: remove the test_db_path after the test
    if test_db_path.exists():
        test_db_path.unlink()

def test_app_add_and_list_task():
    """Test adding a task and then listing it."""
    # Add a task
    result = runner.invoke(app, ["add", "Buy milk", "--priority", "1", "--category", "shopping"])
    assert result.exit_code == 0
    assert "Task added: Buy milk (ID: 1)" in result.stdout

    # List tasks and check if the added task is present
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Buy milk" in result.stdout
    assert "shopping" in result.stdout
    assert "ID: 1" in result.stdout

def test_app_list_empty():
    """Test listing tasks when no tasks are present."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No tasks found." in result.stdout

def test_app_edit_task():
    """Test editing an existing task."""
    runner.invoke(app, ["add", "Original task title"])
    result = runner.invoke(app, ["edit", "1", "--title", "Updated task title", "--priority", "2"])
    assert result.exit_code == 0
    assert "Task ID 1 updated:" in result.stdout
    assert "Updated task title" in result.stdout
    assert "Priority: 2" in result.stdout

    result = runner.invoke(app, ["list"])
    assert "Updated task title" in result.stdout
    assert "Priority: 2" in result.stdout

def test_app_complete_task():
    """Test marking a task as complete."""
    runner.invoke(app, ["add", "Task to complete"])
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "Task ID 1 marked as complete:" in result.stdout
    assert "✅ ID: 1" in result.stdout

    result = runner.invoke(app, ["list"])
    assert "✅ ID: 1" in result.stdout
    assert "Task to complete" in result.stdout

def test_app_delete_task():
    """Test deleting a task."""
    runner.invoke(app, ["add", "Task to delete"])
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "Task ID 1 deleted successfully." in result.stdout

    result = runner.invoke(app, ["list"])
    assert "No tasks found." in result.stdout

def test_app_search_task():
    """Test searching for tasks by keyword."""
    runner.invoke(app, ["add", "Task with keyword alpha"])
    runner.invoke(app, ["add", "Another task beta"])
    runner.invoke(app, ["add", "Final task gamma"])

    result = runner.invoke(app, ["search", "alpha"])
    assert result.exit_code == 0
    assert "Task with keyword alpha" in result.stdout
    assert "Another task beta" not in result.stdout

    result = runner.invoke(app, ["search", "gamma"])
    assert result.exit_code == 0
    assert "Final task gamma" in result.stdout
    assert "Task with keyword alpha" not in result.stdout

def test_app_search_task_no_results():
    """Test searching for tasks with no matching results."""
    runner.invoke(app, ["add", "Some task"])
    result = runner.invoke(app, ["search", "nonexistent"])
    assert result.exit_code == 0
    assert "No tasks found matching 'nonexistent'." in result.stdout

def test_app_edit_non_existent_task():
    """Test editing a task that does not exist."""
    result = runner.invoke(app, ["edit", "999", "--title", "Non-existent"])
    assert result.exit_code == 0
    assert "Error: Task with ID 999 not found." in result.stdout

def test_app_delete_non_existent_task():
    """Test deleting a task that does not exist."""
    result = runner.invoke(app, ["delete", "999"])
    assert result.exit_code == 0
    assert "Error: Task with ID 999 not found." in result.stdout

def test_app_complete_non_existent_task():
    """Test completing a task that does not exist."""
    result = runner.invoke(app, ["complete", "999"])
    assert result.exit_code == 0
    assert "Error: Task with ID 999 not found." in result.stdout

def test_app_add_with_due_date_and_category():
    """Test adding a task with due date and category and then listing it."""
    runner.invoke(app, ["add", "Task with due date", "-d", "2026-04-01", "-c", "planning"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task with due date" in result.stdout
    assert "Due: 2026-04-01" in result.stdout
    assert "Category: planning" in result.stdout

def test_app_list_by_category():
    """Test listing tasks filtered by category."""
    runner.invoke(app, ["add", "Work task 1", "-c", "work"])
    runner.invoke(app, ["add", "Personal task 1", "-c", "personal"])
    runner.invoke(app, ["add", "Work task 2", "-c", "work"])

    result = runner.invoke(app, ["list", "-c", "work"])
    assert result.exit_code == 0
    assert "Work task 1" in result.stdout
    assert "Work task 2" in result.stdout
    assert "Personal task 1" not in result.stdout
