"""タスクの永続化（JSON）を扱う。"""

from __future__ import annotations

import json
from pathlib import Path

from .models import Task


def load_tasks(path: Path) -> list[Task]:
    """ストレージからタスク一覧を読み込む。"""
    if not path.exists():
        return []
    if path.suffix not in {".json"}:
        raise ValueError("Only .json storage is supported for now")
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw) if raw.strip() else []
    return [Task.from_dict(item) for item in data]


def save_tasks(path: Path, tasks: list[Task]) -> None:
    """タスク一覧をストレージへ保存する。"""
    if path.suffix not in {".json"}:
        raise ValueError("Only .json storage is supported for now")
    payload = [task.to_dict() for task in tasks]
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
