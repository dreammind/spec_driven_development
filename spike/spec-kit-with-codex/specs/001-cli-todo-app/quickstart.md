# Quickstart: CLI版TODOタスク管理

## 1. 開発環境準備

```bash
cd /Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex
uv sync
# 必要に応じて依存を追加する場合
# uv add pydantic pytest mypy
```

## 2. 想定実行コマンド

```bash
# タスク追加
uv run python -m todo_cli.cli add --title "牛乳を買う"

# 既定一覧（未完了のみ）
uv run python -m todo_cli.cli list

# 完了済みを含む一覧
uv run python -m todo_cli.cli list --all-active

# 完了化
uv run python -m todo_cli.cli complete --id <uuid>

# 未完了化
uv run python -m todo_cli.cli reopen --id <uuid>

# アーカイブ
uv run python -m todo_cli.cli archive --id <uuid>

# 復元（未完了で戻る）
uv run python -m todo_cli.cli restore --id <uuid>
```

## 3. テスト実行

```bash
uv run pytest -q
# カバレッジ90%以上をゲートにする
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

## 4. 型チェック実行

```bash
uv run mypy src tests
```

## 5. 受け入れ確認チェック

- 空タイトル追加が拒否される
- 不正/未存在UUIDで更新系コマンドが失敗する
- `archive` 後に既定一覧から非表示になる
- `restore` 後に未完了で再表示される
- 再起動後もデータが保持される
- Pydanticの検証エラーがユーザー向けに分かりやすく表示される
- `uv run mypy src tests` がエラー0件で完了する
- `uv run pytest --cov=src --cov-fail-under=90` が成功する
