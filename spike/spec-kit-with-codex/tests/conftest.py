from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from todo_cli.cli import run


@pytest.fixture
def storage_path(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


@pytest.fixture
def run_cli(storage_path: Path) -> Callable[..., int]:
    def _run(*argv: str) -> int:
        return run([*argv, "--storage", str(storage_path)])

    return _run
