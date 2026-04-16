from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

TASK_TITLE_MAX_LENGTH = 255


class Task(BaseModel):
    id: UUID
    title: str
    is_completed: bool = False
    is_archived: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return cls.normalize_title(value)

    @staticmethod
    def normalize_title(value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("title must not be empty")
        if len(title) > TASK_TITLE_MAX_LENGTH:
            raise ValueError(f"title must be at most {TASK_TITLE_MAX_LENGTH} characters")
        return title

    def complete(self) -> "Task":
        return self.model_copy(update={"is_completed": True})

    def reopen(self) -> "Task":
        return self.model_copy(update={"is_completed": False})

    def archive(self) -> "Task":
        return self.model_copy(update={"is_archived": True})

    def restore(self) -> "Task":
        # Clarified behavior: restore always resets completion to incomplete.
        return self.model_copy(update={"is_archived": False, "is_completed": False})


class TaskCollection(BaseModel):
    tasks: list[Task] = Field(default_factory=list)
