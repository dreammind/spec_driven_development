# Quickstart: タスクタイトル編集機能

## 1. セットアップ

```bash
cd /Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex
uv sync
```

## 2. 機能確認コマンド

```bash
# 既存タスクを作成
uv run todo add --title "旧タイトル"

# タイトル編集
uv run todo edit --id <uuid> --title "新タイトル"

# 一覧確認
uv run todo list --all-active
```

## 3. 不正ケース確認

```bash
# 空タイトル
uv run todo edit --id <uuid> --title "   "

# 255文字超過タイトル
uv run todo edit --id <uuid> --title "<256文字以上>"

# 不正ID
uv run todo edit --id bad-id --title "x"
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

## 6. 実施結果 (2026-04-16)

- US1: PASS（対象IDのタイトルのみ更新、他タスク不変を確認）
- US2: PASS（一覧表示と再起動後の保持、完了状態維持を確認）
- US3: PASS（不正ID/空白/255文字超過/未存在/アーカイブ済み編集を拒否しデータ不変を確認）
- 品質ゲート: PASS（`pytest` 29件成功、カバレッジ 97.47%、`mypy` エラー 0件）
