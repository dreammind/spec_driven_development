"""CLI エントリポイント。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

from .commands.add import add_task
from .commands.delete import delete_task
from .commands.done import mark_done
from .commands.edit import edit_task
from .commands.list import list_tasks
from .commands.search import search_tasks
from .commands.undo import mark_open

DEFAULT_STORAGE = Path("tasks.json")


def _print_tasks(tasks: Iterable) -> None:
    for task in tasks:
        due = task.due_date or "-"
        cats = f" #{'#'.join(task.categories)}" if task.categories else ""
        print(f"{task.id} [{task.status}] ({task.priority}) {due} {task.title}{cats}")


def build_parser() -> argparse.ArgumentParser:
    """CLI引数パーサを構築する。"""
    parser = argparse.ArgumentParser(prog="todo")
    parser.add_argument(
        "--storage",
        type=Path,
        default=DEFAULT_STORAGE,
        help="Path to tasks.json",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("title")
    add_parser.add_argument("--description")
    add_parser.add_argument("--priority", required=True, choices=["high", "medium", "low"])
    add_parser.add_argument("--due")
    add_parser.add_argument("--category")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", default="all", choices=["all", "open", "done"])
    list_parser.add_argument("--priority", choices=["high", "medium", "low"])
    list_parser.add_argument("--category")
    list_parser.add_argument("--sort", choices=["due", "priority", "created"])
    list_parser.add_argument("--overdue", action="store_true")

    done_parser = subparsers.add_parser("done", help="Mark task done")
    done_parser.add_argument("id")

    undo_parser = subparsers.add_parser("undo", help="Mark task open")
    undo_parser.add_argument("id")

    delete_parser = subparsers.add_parser("delete", help="Delete task")
    delete_parser.add_argument("id")

    edit_parser = subparsers.add_parser("edit", help="Edit task")
    edit_parser.add_argument("id")
    edit_parser.add_argument("--title")
    edit_parser.add_argument("--description")
    edit_parser.add_argument("--priority", choices=["high", "medium", "low"])
    edit_parser.add_argument("--due")
    edit_parser.add_argument("--category")

    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("keyword")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLIの実行入口。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    storage_path: Path = args.storage

    if args.command == "add":
        categories = args.category.split(",") if args.category else None
        task = add_task(
            storage_path,
            args.title,
            description=args.description,
            priority=args.priority,
            due_date=args.due,
            categories=categories,
        )
        print(f"Added task: {task.id} \"{task.title}\"")
        return 0

    if args.command == "list":
        tasks = list_tasks(
            storage_path,
            status=args.status,
            priority=args.priority,
            category=args.category,
            sort=args.sort,
            overdue=args.overdue,
        )
        _print_tasks(tasks)
        return 0

    if args.command == "done":
        task = mark_done(storage_path, args.id)
        print(f"Marked done: {task.id}")
        return 0

    if args.command == "undo":
        task = mark_open(storage_path, args.id)
        print(f"Marked open: {task.id}")
        return 0

    if args.command == "delete":
        task = delete_task(storage_path, args.id)
        print(f"Deleted: {task.id}")
        return 0

    if args.command == "edit":
        categories = args.category.split(",") if args.category else None
        task = edit_task(
            storage_path,
            args.id,
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=args.due,
            categories=categories,
        )
        print(f"Updated: {task.id}")
        return 0

    if args.command == "search":
        tasks = search_tasks(storage_path, args.keyword)
        _print_tasks(tasks)
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
