# ディレクトリ構成案

以下はPython・TDD前提でのシンプルな構成案です（フラット構成）。

- `todo_cli/`
- `todo_cli/__init__.py`
- `todo_cli/cli.py`（コマンド入口）
- `todo_cli/commands/`（add/list/done/undo/delete/edit/search）
- `todo_cli/commands/__init__.py`
- `todo_cli/models.py`（Taskスキーマ）
- `todo_cli/storage.py`（JSON読み書き）
- `tests/`
- `tests/conftest.py`
- `tests/test_add.py`
- `tests/test_cli.py`
- `tests/test_delete.py`
- `tests/test_done_undo.py`
- `tests/test_edit.py`
- `tests/test_list.py`
- `tests/test_search.py`
