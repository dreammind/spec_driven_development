from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from todo_cli.app import TodoApp
from todo_cli.repository import (
    TaskEditArchivedError,
    InvalidTaskIdError,
    TaskAlreadyArchivedError,
    TaskNotArchivedError,
    TaskNotFoundError,
    TaskValidationError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="CLI TODO manager")
    parser.add_argument(
        "--storage",
        type=Path,
        default=Path(".todo/tasks.json"),
        help="Path to the task storage JSON file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_cmd = subparsers.add_parser("add", help="Add a new task")
    add_cmd.add_argument("--title", required=True, help="Task title")

    list_cmd = subparsers.add_parser("list", help="List tasks")
    list_cmd.add_argument(
        "--all-active",
        action="store_true",
        help="Include completed active tasks",
    )

    complete_cmd = subparsers.add_parser("complete", help="Mark task as completed")
    complete_cmd.add_argument("--id", required=True, help="Task ID (UUID)")

    reopen_cmd = subparsers.add_parser("reopen", help="Mark task as incomplete")
    reopen_cmd.add_argument("--id", required=True, help="Task ID (UUID)")

    archive_cmd = subparsers.add_parser("archive", help="Archive task")
    archive_cmd.add_argument("--id", required=True, help="Task ID (UUID)")

    restore_cmd = subparsers.add_parser("restore", help="Restore archived task")
    restore_cmd.add_argument("--id", required=True, help="Task ID (UUID)")

    edit_cmd = subparsers.add_parser("edit", help="Edit task title")
    edit_cmd.add_argument("--id", required=True, help="Task ID (UUID)")
    edit_cmd.add_argument("--title", required=True, help="New task title")

    return parser


def _print_task(task_id: str, title: str, completed: bool, archived: bool) -> None:
    print(f"{task_id} | {title} | completed={completed} | archived={archived}")


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    app = TodoApp(storage_path=args.storage)

    try:
        if args.command == "add":
            task = app.add_task(args.title)
            print(f"added: {task.id} | {task.title}")
            return 0

        if args.command == "list":
            tasks = app.list_tasks(include_completed=args.all_active)
            if not tasks:
                print("No tasks found.")
                return 0
            for task in tasks:
                _print_task(str(task.id), task.title, task.is_completed, task.is_archived)
            return 0

        if args.command == "complete":
            task = app.complete_task(args.id)
            print(f"completed: {task.id}")
            return 0

        if args.command == "reopen":
            task = app.reopen_task(args.id)
            print(f"reopened: {task.id}")
            return 0

        if args.command == "archive":
            task = app.archive_task(args.id)
            print(f"archived: {task.id}")
            return 0

        if args.command == "restore":
            task = app.restore_task(args.id)
            print(f"restored: {task.id}")
            return 0

        if args.command == "edit":
            task = app.edit_task_title(args.id, args.title)
            print(f"edited: {task.id} | {task.title}")
            return 0

        parser.print_help()
        return 2
    except (
        InvalidTaskIdError,
        TaskNotFoundError,
        TaskAlreadyArchivedError,
        TaskNotArchivedError,
        TaskEditArchivedError,
        TaskValidationError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"unexpected error: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
