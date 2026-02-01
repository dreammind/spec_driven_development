# TODO CLI アプリケーション 設計書

## 1. 概要
本ドキュメントは、`doc/Requirement.md` に基づき、TODO CLIアプリケーションの技術的な設計を定義します。

## 2. 技術選定
- **言語**: Python 3.10+
- **CLIフレームワーク**: Typer (型ヒントとの親和性が高く、堅牢なCLIを容易に構築できるため)
- **テストフレームワーク**: Pytest (豊富なプラグインとシンプルな記法が特徴)
- **テストカバレッジ**: pytest-cov
- **型チェック**: Mypy (型安全性とコード品質の向上のため)
- **依存関係管理**: Poetry

## 3. プロジェクト構成
```
todo_cli/
├── src/
│   ├── todo/
│   │   ├── __init__.py
│   │   ├── main.py        # Typerアプリケーションのエントリポイント
│   │   ├── models.py      # データモデル(Taskクラス)
│   │   ├── database.py    # tasks.jsonへの読み書きロジック
│   │   └── manager.py     # TaskManagerなどの中核ロジック
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   └── test_manager.py
├── .gitignore
├── pyproject.toml     # (Poetryを使用する場合)
└── tasks.json         # データストア (初回実行時に自動生成)
```

## 4. データモデル (`src/todo/models.py`)
タスク情報を格納するためのPydanticモデルを定義します。これにより、型安全性が向上し、データのバリデーションが容易になります。

```python
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    priority: int = Field(ge=1, le=5, default=3) # 1(高) ~ 5(低)
    due_date: Optional[date] = None
    category: str = "default"
    is_completed: bool = False
```

## 5. 設計詳細

### 5.1. データ永続化層 (`src/todo/database.py`)
`tasks.json` ファイルへの読み書きを責務とします。

- `load_tasks() -> List[Task]`: `tasks.json` が存在すれば読み込んで `List[Task]` を返す。存在しなければ空のリストを返す。
- `save_tasks(tasks: List[Task])`: `List[Task]` を `tasks.json` に上書き保存する。

### 5.2. コアロジック層 (`src/todo/manager.py`)
アプリケーションのビジネスロジックをカプセル化します。

- `TaskManager` クラス:
    - `__init__()`: `database`モジュールを介してタスクをロードする。
    - `_save()`: 現在のタスクリストを保存する内部メソッド。
    - `get_next_id() -> int`: 新規タスク用のIDを採番する。
    - `add_task(...) -> Task`: 新規タスクを追加して保存する。
    - `edit_task(...) -> Optional[Task]`: 既存タスクを編集して保存する。
    - `delete_task(task_id: int) -> bool`: タスクを削除して保存する。
    - `complete_task(task_id: int) -> Optional[Task]`: タスクを完了状態にする。
    - `list_tasks(...) -> List[Task]`: タスクをフィルタリング・ソートして返す。
    - `search_tasks(keyword: str) -> List[Task]`: タイトルでキーワード検索を行う。

### 5.3. プレゼンテーション層 (`src/todo/main.py`)
Typerを使用して、ユーザーからの入力を受け付け、`TaskManager` を呼び出します。

- `typer.Typer()` アプリケーションを定義。
- 各機能要件に対応するコマンドを `@app.command()` で定義。
    - `add(title: str, priority: int, ...)`
    - `edit(task_id: int, ...)`
    - `delete(task_id: int)`
    - `complete(task_id: int)`
    - `list(category: str, sort_by: str)`
    - `search(keyword: str)`
- 各コマンドは `TaskManager` のインスタンスを生成し、対応するメソッドを呼び出し、結果を整形してコンソールに出力します。
