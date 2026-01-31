"""タスク検索コマンドの実装。"""

from __future__ import annotations

from pathlib import Path

from ..models import Task
from ..storage import load_tasks


def search_tasks(storage_path: Path, keyword: str) -> list[Task]:
    """キーワードに一致するタスクを返す。"""
    if not keyword or not keyword.strip():
        raise ValueError("keyword is required")
    term = keyword.strip().lower()

    tasks = load_tasks(storage_path)
    results: list[Task] = []
    for task in tasks:
        haystack = f"{task.title}\n{task.description or ''}".lower()
        if term in haystack:
            results.append(task)
    return results
