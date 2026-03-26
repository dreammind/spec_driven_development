# 設計書 — CLIタスク管理（TODO）アプリ

## 次の目的

本設計書をもとに、実装計画書（[doc/ImplementationPlan.md](doc/ImplementationPlan.md)）を作成してください。

## 1. 技術スタック

| 項目 | 選定内容 | 理由 |
|---|---|---|
| 言語 | Python 3.11以上 | 型ヒントが充実しており、型安全性を確保しやすい |
| CLIフレームワーク | [Typer](https://typer.tiangolo.com/) | 型ヒントベースでCLIを構築でき、ヘルプ自動生成に対応 |
| データ形式 | JSON（`tasks.json`） | 標準ライブラリのみで読み書き可能 |
| 型チェック | mypy | 静的型検査によるバグ防止 |
| テスト | pytest | カバレッジ計測（pytest-cov）に対応 |
| パッケージ管理 | uv | 高速な依存関係管理 |

---

## 2. プロジェクト構成

```
todo_cli/
├── pyproject.toml          # パッケージ設定・依存関係
├── tasks.json              # データ保存ファイル（自動生成）
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       ├── main.py         # CLIエントリーポイント（Typerアプリ定義）
│       ├── models.py       # データモデル（Task, Priority）
│       ├── repository.py   # データの読み書き（tasks.json操作）
│       ├── service.py      # ビジネスロジック
│       └── display.py      # 一覧・詳細の表示フォーマット
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_repository.py
    ├── test_service.py
    └── test_display.py
```

---

## 3. データモデル

### 3.1 Priority（列挙型）

```python
class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

### 3.2 Task（データクラス）

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `id` | `str` | 必須 | UUID v4 |
| `title` | `str` | 必須 | タスクのタイトル |
| `done` | `bool` | 必須 | 完了フラグ（デフォルト: `False`） |
| `priority` | `Priority` | 必須 | 優先度（デフォルト: `MEDIUM`） |
| `due_date` | `date \| None` | 任意 | 期限日 |
| `category` | `str \| None` | 任意 | カテゴリ名 |
| `created_at` | `datetime` | 必須 | 作成日時 |
| `updated_at` | `datetime` | 必須 | 更新日時 |
| `deleted_at` | `datetime \| None` | 必須 | 論理削除日時（`None` = 未削除） |

### 3.3 tasks.json フォーマット

```json
[
  {
    "id": "a1b2c3d4-...",
    "title": "レポートを提出する",
    "done": false,
    "priority": "high",
    "due_date": "2026-03-31",
    "category": "仕事",
    "created_at": "2026-03-25T10:00:00",
    "updated_at": "2026-03-25T10:00:00"
  }
]
```

---

## 4. アーキテクチャ

レイヤードアーキテクチャを採用します。

```
[CLI層] main.py
    ↓ コマンド引数を受け取り、Serviceを呼び出す
[サービス層] service.py
    ↓ ビジネスロジック（バリデーション、フィルタリング、検索など）
[リポジトリ層] repository.py
    ↓ tasks.json の読み書き
[モデル層] models.py
    タスクのデータ構造定義
```

各層の責務：

| 層 | ファイル | 責務 |
|---|---|---|
| CLI層 | `main.py` | コマンド定義・引数解析・エラーハンドリング・表示呼び出し |
| サービス層 | `service.py` | タスクの追加・更新・削除・検索・フィルタリングのロジック |
| リポジトリ層 | `repository.py` | `tasks.json` の読み込み・書き込み |
| モデル層 | `models.py` | `Task`・`Priority` の型定義 |
| 表示層 | `display.py` | CLIへの出力フォーマット |

---

## 5. CLIコマンド設計

### 基本構文

```
todo <コマンド> [引数] [オプション]
```

### コマンド一覧

| コマンド | 引数 | オプション | 説明 |
|---|---|---|---|
| `add` | `TITLE` | `--priority`, `--due-date`, `--category` | タスクを追加 |
| `list` | — | `--done`, `--undone`, `--priority`, `--category`, `--overdue`, `--sort` | タスク一覧表示 |
| `show` | `ID` | — | タスク詳細表示 |
| `done` | `ID` | — | タスクを完了にする |
| `edit` | `ID` | `--title`, `--priority`, `--due-date`, `--category` | タスクを編集 |
| `delete` | `ID` | — | タスクを論理削除（`deleted_at` に削除日時を記録） |
| `search` | `KEYWORD` | — | タイトルをキーワードで検索 |

### コマンド詳細

#### `add`
```
todo add "レポートを提出する" --priority high --due-date 2026-03-31 --category 仕事
```

#### `list`
```
todo list                        # 全タスク表示
todo list --undone               # 未完了のみ
todo list --priority high        # 優先度:高のみ
todo list --category 仕事        # カテゴリ:仕事のみ
todo list --overdue              # 期限切れのみ
todo list --sort priority        # 優先度順で並べ替え
```

#### `search`
```
todo search "レポート"
```

---

## 6. エラーハンドリング

| エラー条件 | 表示メッセージ例 |
|---|---|
| 存在しないIDを指定 | `Error: タスクID "xxx" が見つかりません` |
| 不正な日付フォーマット | `Error: 日付は YYYY-MM-DD 形式で入力してください` |
| 不正な優先度値 | `Error: 優先度は high / medium / low のいずれかを指定してください` |
| 検索結果が0件 | `該当するタスクが見つかりませんでした` |
| データファイル読み込み失敗 | `Error: データファイルの読み込みに失敗しました` |

---

## 7. テスト方針

| 対象 | テスト内容 |
|---|---|
| `models.py` | `Task`・`Priority` の生成・バリデーション |
| `repository.py` | `tasks.json` の読み書き、ファイル不在時の初期化 |
| `service.py` | 追加・完了・削除・編集・検索・フィルタリングの各ロジック |
| `display.py` | 出力フォーマットの正確性 |

- テストカバレッジ 90% 以上を目標とする
- `pytest-cov` でカバレッジを計測する
- テストはユニットテストを基本とし、`tasks.json` の読み書きは一時ディレクトリを使用する

---

## 8. 非機能設計

### 型安全性

- すべてのモジュールで型ヒントを付与する
- `mypy --strict` で型チェックをパスすることを目標とする

### データ保存

- `tasks.json` が存在しない場合は初回起動時に自動生成する
- 書き込みは常に全データを上書きする（アトミック性は保証しない）
- 削除は論理削除とし、`deleted_at` に削除日時を記録する（データは `tasks.json` に残る）
- `list` / `show` / `search` などの通常操作では `deleted_at` が `None` のタスクのみを対象とする

### パフォーマンス

- 想定データ件数は最大 1,000 件程度とし、インメモリ操作で十分なパフォーマンスを確保する
