# タスク管理（TODO）CLIアプリ 設計書（コマンド: uv run todo）

## 1. システム概要

- Python製CLIアプリケーションとして実装
- コマンドラインからタスクの追加・一覧表示・完了・編集・削除が可能
- タスクデータはローカルの `tasks.json` に保存
- 型安全性・テスト容易性を重視

---

## 2. ディレクトリ構成（例）

```
todo_cli/
├── src/
│   ├── todo.py         # CLIエントリポイント（実行ファイル名をtodo.pyに変更）
│   ├── models.py       # タスクデータモデル（pydantic利用）
│   ├── storage.py      # JSONファイル入出力
│   ├── commands/
│   │   ├── add.py
│   │   ├── list.py
│   │   ├── done.py
│   │   ├── edit.py
│   │   └── delete.py
│   └── utils.py        # 補助関数
├── tests/
│   ├── test_add.py
│   ├── test_list.py
│   ├── test_done.py
│   ├── test_edit.py
│   └── test_delete.py
├── tasks.json          # タスクデータ保存ファイル
├── pyproject.toml      # 依存管理（uv対応）
└── README.md
```

---

## 3. データモデル設計

`src/models.py` でpydanticを利用し、型安全かつバリデーション可能なモデルを定義します。

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    detail: Optional[str] = None
    priority: str  # '高', '中', '低' のいずれか
    due: Optional[date] = None
    categories: List[str] = []
    done: bool = False
```

---

## 4. コマンド設計

| コマンド例                                 | 機能概要                              | 主な引数・オプション例           |
|--------------------------------------------|--------------------------------------|----------------------------------|
| `uv run todo add`                         | タスク追加                            | --name, --detail, --priority, --due, --category |
| `uv run todo list`                        | タスク一覧表示                        | --priority, --due, --category, --done |
| `uv run todo done <id>`                   | タスク完了                            | タスクID                         |
| `uv run todo edit <id>`                   | タスク編集                            | --name, --detail, --priority, --due, --category |
| `uv run todo delete <id>`                 | タスク削除                            | タスクID                         |

- コマンド実装には [typer](https://typer.tiangolo.com/) を推奨
- 実行ファイルは `src/todo.py` とし、`pyproject.toml` の `[tool.uv.scripts]` で `todo = 'src/todo.py'` を設定

---

## 5. ストレージ設計

- タスクデータは `tasks.json` に配列として保存
- 読み込み時は全件ロード、書き込み時は全件上書き
- ファイルが存在しない場合は自動生成

---

## 6. バリデーション・制約

- タスク名・優先度は必須
- 優先度は「高」「中」「低」のいずれか
- 期限は日付形式（YYYY-MM-DD）
- カテゴリは0個以上の文字列リスト
- 編集時も同様のバリデーションを実施

---

## 7. テスト設計

- pytestによるユニットテスト・統合テスト
- 各コマンドごとに正常系・異常系テストを用意
- テストカバレッジ90%以上を目標

---

## 8. 型チェック

- mypyによる型チェックをCIに組み込み

---

## 9. 開発環境

- Python 3.9以上
- uvによる仮想環境・依存管理
- 必要パッケージ: typer, pydantic, pytest, mypy など

---

## 10. コマンド実行例

```sh
uv run todo add --name "買い物" --priority "高" --due "2024-06-30"
uv run todo list --priority "高"
uv run todo done 123e4567-e89b-12d3-a456-426614