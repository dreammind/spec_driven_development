from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date
import uuid


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    detail: Optional[str] = None
    priority: str  # '高', '中', '低' のいずれか
    due: Optional[date] = None
    categories: List[str] = []
    done: bool = False

    @validator("priority")
    def validate_priority(cls, v):
        if v not in {"高", "中", "低"}:
            raise ValueError("priority must be '高', '中', or '低'")
        return v
