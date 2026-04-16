# Quickstart: タスクタイトル編集機能

## 1. セットアップ

```bash
cd /Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex
uv sync
```

## 2. 機能確認コマンド

```bash
# 既存タスクを作成
uv run python -m todo_cli.cli add --title "旧タイトル"

# タイトル編集
uv run python -m todo_cli.cli edit --id <uuid> --title "新タイトル"

# 一覧確認
uv run python -m todo_cli.cli list --all-active
```

## 3. 不正ケース確認

```bash
# 空タイトル
uv run python -m todo_cli.cli edit --id <uuid> --title "   "

# 255文字超過タイトル
uv run python -m todo_cli.cli edit --id <uuid> --title "<256文字以上>"

# 不正ID
uv run python -m todo_cli.cli edit --id bad-id --title "x"
```

## 4. テスト・品質ゲート

```bash
uv run pytest -q
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90
uv run mypy src tests
```

## 5. 受け入れ確認

- 編集成功時にタイトルのみ更新される
- 編集失敗時に既存データが保持される
- アーカイブ済みタスク編集が拒否される
- 再起動後も編集済みタイトルが保持される
- `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90` が成功する
- `uv run mypy src tests` が成功し、型チェックエラー0件である
