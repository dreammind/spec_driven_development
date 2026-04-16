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


def test_edit_single_task_keeps_others_unchanged(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "t1"]) == 0
    first_id = capsys.readouterr().out.split("added:")[1].split("|")[0].strip()
    assert run(["--storage", str(storage), "add", "--title", "t2"]) == 0
    second_id = capsys.readouterr().out.split("added:")[1].split("|")[0].strip()

    assert run(["--storage", str(storage), "edit", "--id", first_id, "--title", "t1-new"]) == 0
    assert run(["--storage", str(storage), "list", "--all-active"]) == 0
    out = capsys.readouterr().out
    assert first_id in out and "t1-new" in out
    assert second_id in out and "t2" in out


def test_edit_persists_after_restart_and_keeps_completion_state(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "t1"]) == 0
    task_id = capsys.readouterr().out.split("added:")[1].split("|")[0].strip()
    assert run(["--storage", str(storage), "complete", "--id", task_id]) == 0
    capsys.readouterr()

    assert run(["--storage", str(storage), "edit", "--id", task_id, "--title", "updated"]) == 0
    capsys.readouterr()

    assert run(["--storage", str(storage), "list", "--all-active"]) == 0
    out = capsys.readouterr().out
    assert task_id in out
    assert "updated" in out
    assert "completed=True" in out


def test_edit_failures_do_not_mutate_data(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "safe"]) == 0
    task_id = capsys.readouterr().out.split("added:")[1].split("|")[0].strip()

    assert run(["--storage", str(storage), "edit", "--id", task_id, "--title", "   "]) == 2
    capsys.readouterr()
    assert run(["--storage", str(storage), "edit", "--id", task_id, "--title", "x" * 256]) == 2
    capsys.readouterr()
    assert run(["--storage", str(storage), "edit", "--id", "bad-id", "--title", "x"]) == 2
    capsys.readouterr()
    assert run(
        [
            "--storage",
            str(storage),
            "edit",
            "--id",
            "cb5f4da4-8ba6-4ce9-9b58-849534f4f5d3",
            "--title",
            "x",
        ]
    ) == 2
    capsys.readouterr()
    assert run(["--storage", str(storage), "archive", "--id", task_id]) == 0
    capsys.readouterr()
    assert run(["--storage", str(storage), "edit", "--id", task_id, "--title", "x"]) == 2
    capsys.readouterr()

    assert run(["--storage", str(storage), "restore", "--id", task_id]) == 0
    capsys.readouterr()
    assert run(["--storage", str(storage), "list", "--all-active"]) == 0
    out = capsys.readouterr().out
    assert "safe" in out
