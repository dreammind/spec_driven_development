"""CLI 結線のテスト。"""

from __future__ import annotations

from pathlib import Path

from todo_cli import cli


def _capture_output(capsys) -> str:
    return capsys.readouterr().out.strip()


def test_cli_add_list_done_undo_delete(capsys, tmp_path: Path) -> None:
    """CLIの主要フローを一通り確認する。"""
    storage = tmp_path / "tasks.json"

    assert cli.main(["--storage", str(storage), "add", "Write spec", "--priority", "high"]) == 0
    out = _capture_output(capsys)
    assert out.startswith("Added task:")
    task_id = out.split()[2]

    assert cli.main(["--storage", str(storage), "list"]) == 0
    out = _capture_output(capsys)
    assert task_id in out

    assert cli.main(["--storage", str(storage), "done", task_id]) == 0
    out = _capture_output(capsys)
    assert out == f"Marked done: {task_id}"

    assert cli.main(["--storage", str(storage), "undo", task_id]) == 0
    out = _capture_output(capsys)
    assert out == f"Marked open: {task_id}"

    assert cli.main(["--storage", str(storage), "delete", task_id]) == 0
    out = _capture_output(capsys)
    assert out == f"Deleted: {task_id}"


def test_cli_edit_and_search(capsys, tmp_path: Path) -> None:
    """CLIの編集と検索を確認する。"""
    storage = tmp_path / "tasks.json"

    assert cli.main(["--storage", str(storage), "add", "Prepare slides", "--priority", "medium"]) == 0
    out = _capture_output(capsys)
    task_id = out.split()[2]

    assert (
        cli.main(
            [
                "--storage",
                str(storage),
                "edit",
                task_id,
                "--title",
                "Prepare keynote",
                "--priority",
                "high",
                "--category",
                "work",
            ]
        )
        == 0
    )
    out = _capture_output(capsys)
    assert out == f"Updated: {task_id}"

    assert cli.main(["--storage", str(storage), "search", "keynote"]) == 0
    out = _capture_output(capsys)
    assert task_id in out
