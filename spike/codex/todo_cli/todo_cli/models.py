from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Optional

Priority = Literal["high", "medium", "low"]
Status = Literal["open", "done"]


@dataclass(frozen=True)
class Task:
    """タスクの不変データモデル（作成後に変更しない前提）。"""
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    due_date: Optional[str]
    categories: list[str]
    status: Status
    created_at: str
    completed_at: Optional[str]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Task":
        return Task(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            priority=data["priority"],
            due_date=data.get("due_date"),
            categories=list(data.get("categories", [])),
            status=data["status"],
            created_at=data["created_at"],
            completed_at=data.get("completed_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "categories": list(self.categories),
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


def now_iso_utc() -> str:
    """UTCの現在時刻をISO 8601で返す（Zサフィックス）。"""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
