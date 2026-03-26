from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    id: str
    title: str
    done: bool
    priority: Priority
    created_at: datetime
    updated_at: datetime
    due_date: date | None = None
    category: str | None = None
    deleted_at: datetime | None = None

    @classmethod
    def create(
        cls,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
        category: str | None = None,
    ) -> Task:
        now = datetime.now()
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            done=False,
            priority=priority,
            created_at=now,
            updated_at=now,
            due_date=due_date,
            category=category,
            deleted_at=None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return cls(
            id=data["id"],
            title=data["title"],
            done=data["done"],
            priority=Priority(data["priority"]),
            due_date=date.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            category=data.get("category"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            deleted_at=datetime.fromisoformat(data["deleted_at"]) if data.get("deleted_at") else None,
        )
