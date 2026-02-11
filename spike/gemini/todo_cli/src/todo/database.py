import json
from pathlib import Path
from typing import List

from todo.models import Task

DEFAULT_DB_PATH = Path("tasks.json")

def load_tasks(db_path: Path = DEFAULT_DB_PATH) -> List[Task]:
    """
    Loads tasks from a JSON file.
    """
    if not db_path.exists() or db_path.stat().st_size == 0:
        return []
    try:
        content = db_path.read_text(encoding="utf-8")
        tasks_data = json.loads(content)
        # Use Pydantic's model_validate to parse dictionaries into Task objects
        return [Task.model_validate(data) for data in tasks_data]
    except (json.JSONDecodeError, FileNotFoundError) as e:
        # Handle cases where the JSON is malformed or file does not exist (though checked above)
        # For now, return empty list on error.
        print(f"Error loading tasks from {db_path}: {e}")
        return []


def save_tasks(tasks: List[Task], db_path: Path = DEFAULT_DB_PATH):
    """
    Saves tasks to a JSON file.
    """
    # Convert Pydantic models to JSON-compatible dictionaries
    # model_dump(mode='json') handles serialization of types like date
    tasks_data = [task.model_dump(mode='json') for task in tasks]
    db_path.write_text(json.dumps(tasks_data, indent=4, ensure_ascii=False), encoding="utf-8")