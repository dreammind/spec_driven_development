# 実装計画書 — CLIタスク管理（TODO）アプリ

## 方針

テスト駆動開発（TDD）で進めます。各ステップは「テスト作成 → 実装 → リファクタリング」のサイクルで完結させてから次へ進んでください。

---

## Phase 1: プロジェクトセットアップ

### Step 1-1: プロジェクト初期化

- [ ] `uv init todo_cli` でプロジェクトを作成
- [ ] `src/todo_cli/` ディレクトリ構成を作成
- [ ] `pyproject.toml` に依存パッケージを追加
  - 本体: `typer`, `rich`
  - 開発用: `pytest`, `pytest-cov`, `mypy`
- [ ] `tests/` ディレクトリと `__init__.py` を作成
- [ ] `pytest` と `mypy` が動作することを確認

---

## Phase 2: モデル層（`models.py`）

### Step 2-1: `Priority` 列挙型

**テスト (`test_models.py`)**
- `Priority.HIGH` / `MEDIUM` / `LOW` が定義されている
- 文字列 `"high"` から `Priority` に変換できる

**実装**
- `Priority(str, Enum)` を定義

---

### Step 2-2: `Task` データクラス

**テスト (`test_models.py`)**
- 必須フィールド（`id`, `title`, `done`, `priority`, `created_at`, `updated_at`, `deleted_at`）を持つ
- `done` のデフォルトが `False`
- `priority` のデフォルトが `Priority.MEDIUM`
- `due_date` / `category` / `deleted_at` のデフォルトが `None`
- `dict` / JSON への変換ができる
- JSON から `Task` を復元できる

**実装**
- `@dataclass` または `pydantic.BaseModel` で `Task` を定義
- `to_dict()` / `from_dict()` メソッドを実装

---

## Phase 3: リポジトリ層（`repository.py`）

### Step 3-1: ファイルの読み書き

**テスト (`test_repository.py`)**
- `tasks.json` が存在しない場合、空リストを返す
- タスクを保存すると `tasks.json` に書き込まれる
- 保存したタスクを読み込むと元のデータが復元される
- 複数タスクの保存・読み込みができる

**実装**
- `load() -> list[Task]`：`tasks.json` を読み込む（なければ空リスト）
- `save(tasks: list[Task]) -> None`：全データを上書き保存
- テストでは `tmp_path` フィクスチャで一時ディレクトリを使用

---

## Phase 4: サービス層（`service.py`）

### Step 4-1: タスク追加

**テスト (`test_service.py`)**
- タイトルを指定してタスクを追加できる
- 追加したタスクに `id` / `created_at` / `updated_at` が自動設定される
- 優先度・期限・カテゴリを指定して追加できる

**実装**
- `add_task(title, priority, due_date, category) -> Task`

---

### Step 4-2: タスク一覧・詳細

**テスト**
- 全タスクを取得できる（論理削除済みは除外される）
- IDでタスクを1件取得できる
- 存在しないIDでは `None` を返す

**実装**
- `list_tasks(filters) -> list[Task]`
- `get_task(id) -> Task | None`

---

### Step 4-3: タスク完了

**テスト**
- `done=True` に更新され `updated_at` が更新される
- 存在しないIDでは例外が発生する

**実装**
- `complete_task(id) -> Task`

---

### Step 4-4: タスク編集

**テスト**
- タイトル・優先度・期限・カテゴリを変更できる
- `updated_at` が更新される
- 存在しないIDでは例外が発生する

**実装**
- `edit_task(id, title, priority, due_date, category) -> Task`

---

### Step 4-5: タスク削除（論理削除）

**テスト**
- `deleted_at` に削除日時が記録される
- 削除済みタスクは `list_tasks` / `search_tasks` に含まれない
- 存在しないIDでは例外が発生する

**実装**
- `delete_task(id) -> Task`

---

### Step 4-6: フィルタリング・並べ替え

**テスト**
- 完了 / 未完了でフィルタリングできる
- 優先度・カテゴリでフィルタリングできる
- 期限切れのみ表示できる
- 優先度順・期限順・作成日順で並べ替えできる

**実装**
- `list_tasks` のフィルタ・ソートオプションを実装

---

### Step 4-7: 検索

**テスト**
- キーワードに部分一致するタスクを返す
- 大文字・小文字を区別しない（オプション）
- 一致なしの場合は空リストを返す

**実装**
- `search_tasks(keyword) -> list[Task]`

---

## Phase 5: 表示層（`display.py`）

### Step 5-1: 一覧表示

**テスト (`test_display.py`)**
- タスク一覧が表形式で出力される
- 期限切れタスクが視覚的に区別される（色や記号）
- 空リストの場合は「タスクがありません」と表示される

**実装**
- `print_task_list(tasks: list[Task]) -> None`（`rich` のテーブルを使用）

---

### Step 5-2: 詳細表示

**テスト**
- タスクの全フィールドが表示される

**実装**
- `print_task_detail(task: Task) -> None`

---

## Phase 6: CLI層（`main.py`）

### Step 6-1: 各コマンドの結合

- [ ] `add` コマンド
- [ ] `list` コマンド（フィルタ・ソートオプション含む）
- [ ] `show` コマンド
- [ ] `done` コマンド
- [ ] `edit` コマンド
- [ ] `delete` コマンド
- [ ] `search` コマンド

各コマンドでエラーハンドリングを実装し、不正入力時にわかりやすいメッセージを表示します。

---

## Phase 7: 品質確認

### Step 7-1: 型チェック

- [ ] `mypy --strict src/` を実行し、型エラーをすべて解消

### Step 7-2: テストカバレッジ

- [ ] `pytest --cov=todo_cli --cov-report=term-missing` を実行
- [ ] カバレッジ 90% 以上を達成

### Step 7-3: 動作確認

- [ ] `todo add` / `list` / `done` / `edit` / `delete` / `search` を手動実行して動作を確認

---

## 実装順序まとめ

```
Phase 1: セットアップ
    ↓
Phase 2: models.py（Priority → Task）
    ↓
Phase 3: repository.py（load / save）
    ↓
Phase 4: service.py（add → list → done → edit → delete → filter → search）
    ↓
Phase 5: display.py（list → detail）
    ↓
Phase 6: main.py（全コマンド結合）
    ↓
Phase 7: 品質確認（mypy / coverage）
```

下位層（モデル・リポジトリ）から順に固めていくことで、上位層のテストが書きやすくなります。
