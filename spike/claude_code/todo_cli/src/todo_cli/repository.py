from __future__ import annotations

import json
from pathlib import Path

from todo_cli.models import Task


class TaskRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> list[Task]:
        if not self._path.exists():
            return []
        with self._path.open(encoding="utf-8") as f:
            data: list[dict[str, object]] = json.load(f)
        return [Task.from_dict(d) for d in data]

    def save(self, tasks: list[Task]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
