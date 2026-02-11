import pytest
from src.models import Task
from datetime import date


def test_create_task_minimal():
    task = Task(name="テスト", priority="高")
    assert task.name == "テスト"
    assert task.priority == "高"
    assert task.done is False


def test_create_task_full():
    task = Task(
        name="詳細テスト",
        detail="詳細説明",
        priority="中",
        due=date(2024, 6, 30),
        categories=["仕事", "重要"],
        done=True,
    )
    assert task.detail == "詳細説明"
    assert task.categories == ["仕事", "重要"]
    assert task.due == date(2024, 6, 30)
    assert task.done is True


def test_priority_validation():
    with pytest.raises(ValueError):
        Task(name="NG", priority="最重要")  # 許可されていない優先度


def test_due_type_validation():
    with pytest.raises(ValueError):
        Task(name="NG", priority="低", due="2024/06/30")  # 日付型でない
