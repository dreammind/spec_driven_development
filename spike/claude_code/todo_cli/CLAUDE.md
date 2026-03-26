# CLAUDE.md — CLIタスク管理（TODO）アプリ

## プロジェクト概要

Pythonで実装したCLIタスク管理アプリ。Typer + Rich を使用し、データはローカルの `~/.todo_cli/tasks.json` に保存する。

## アーキテクチャ

レイヤードアーキテクチャを採用している。

```
[CLI層]        main.py        コマンド定義・引数解析・エラーハンドリング
[サービス層]   service.py     ビジネスロジック（追加・完了・編集・削除・検索）
[リポジトリ層] repository.py  tasks.json の読み書き
[モデル層]     models.py      Task・Priority の型定義
[表示層]       display.py     Rich を使った一覧・詳細表示
```

## 開発コマンド

```bash
# テスト実行
uv run pytest

# カバレッジ付きテスト（目標: 90%以上）
uv run pytest --cov=todo_cli --cov-report=term-missing

# 型チェック
uv run mypy src/

# 動作確認
uv run todo --help
uv run todo add "タスク名"
uv run todo list
```

## コーディングルール

- すべての関数・メソッドに型ヒントを付ける（`mypy --strict` 準拠）
- TDD で進める（テストを先に書いてから実装する）
- テストカバレッジ 90% 以上を維持する

## データに関する注意

- タスクの削除は**論理削除**（`deleted_at` フィールドに削除日時を記録）
- 物理削除は行わない
- `list` / `show` / `search` では `deleted_at is None` のタスクのみ対象とする

## テスト方針

- `tasks.json` の読み書きテストは `tmp_path` フィクスチャで一時ディレクトリを使う
- CLI コマンドのテストは `typer.testing.CliRunner` を使う
- `_DATA_FILE` のパスは `monkeypatch` で差し替える
