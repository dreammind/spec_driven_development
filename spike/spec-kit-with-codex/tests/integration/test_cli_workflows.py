from __future__ import annotations

from pathlib import Path

from pytest import CaptureFixture

from todo_cli.cli import run


def test_add_then_list_default_shows_task(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "buy milk"]) == 0
    assert run(["--storage", str(storage), "list"]) == 0

    out = capsys.readouterr().out
    assert "added:" in out
    assert "buy milk" in out


def test_complete_and_reopen_flow(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "t1"]) == 0
    added_out = capsys.readouterr().out
    task_id = added_out.split("added:")[1].split("|")[0].strip()

    assert run(["--storage", str(storage), "complete", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list", "--all-active"]) == 0
    out_after_complete = capsys.readouterr().out
    assert "completed=True" in out_after_complete

    assert run(["--storage", str(storage), "reopen", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list"]) == 0
    out_after_reopen = capsys.readouterr().out
    assert "completed=False" in out_after_reopen


def test_archive_restore_flow(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "t1"]) == 0
    added_out = capsys.readouterr().out
    task_id = added_out.split("added:")[1].split("|")[0].strip()

    assert run(["--storage", str(storage), "archive", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list"]) == 0
    list_out = capsys.readouterr().out
    assert "No tasks found." in list_out

    assert run(["--storage", str(storage), "restore", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list"]) == 0
    restored_out = capsys.readouterr().out
    assert "completed=False" in restored_out
