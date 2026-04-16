from __future__ import annotations

from pathlib import Path

from pytest import CaptureFixture

from todo_cli.cli import run


def _extract_id(output: str) -> str:
    return output.split("added:")[1].split("|")[0].strip()


def test_add_and_list_contract(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    storage = tmp_path / "tasks.json"
    code = run(["--storage", str(storage), "add", "--title", "milk"])
    assert code == 0
    out = capsys.readouterr().out
    assert "added:" in out

    code = run(["--storage", str(storage), "list"])
    assert code == 0
    out = capsys.readouterr().out
    assert "completed=False" in out
    assert "archived=False" in out


def test_add_empty_title_fails_with_code_2(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    code = run(["--storage", str(storage), "add", "--title", "   "])
    assert code == 2
    err = capsys.readouterr().err
    assert "title" in err


def test_complete_reopen_and_all_active_contract(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "t1"]) == 0
    task_id = _extract_id(capsys.readouterr().out)

    assert run(["--storage", str(storage), "complete", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list", "--all-active"]) == 0
    out = capsys.readouterr().out
    assert "completed=True" in out

    assert run(["--storage", str(storage), "reopen", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list"]) == 0
    out = capsys.readouterr().out
    assert "completed=False" in out


def test_invalid_or_unknown_id_returns_code_2(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    storage = tmp_path / "tasks.json"
    code = run(["--storage", str(storage), "complete", "--id", "bad-id"])
    assert code == 2

    code = run(
        [
            "--storage",
            str(storage),
            "complete",
            "--id",
            "cb5f4da4-8ba6-4ce9-9b58-849534f4f5d3",
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "invalid task id" in err or "task not found" in err


def test_archive_restore_contract(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    storage = tmp_path / "tasks.json"
    assert run(["--storage", str(storage), "add", "--title", "t1"]) == 0
    task_id = _extract_id(capsys.readouterr().out)

    assert run(["--storage", str(storage), "archive", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list"]) == 0
    out = capsys.readouterr().out
    assert "No tasks found." in out

    assert run(["--storage", str(storage), "restore", "--id", task_id]) == 0
    assert run(["--storage", str(storage), "list"] ) == 0
    out = capsys.readouterr().out
    assert "completed=False" in out
