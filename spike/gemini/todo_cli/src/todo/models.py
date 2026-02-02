from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    priority: int = Field(ge=1, le=5, default=3) # 1(高) ~ 5(低)
    due_date: Optional[date] = None
    category: str = "default"
    is_completed: bool = False
