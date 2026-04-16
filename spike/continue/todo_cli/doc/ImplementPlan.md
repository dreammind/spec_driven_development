# タスク管理（TODO）CLIアプリ 実装計画（uv venv不要・uv run運用）

## 1. 開発方針

- Python + uv + typer + pydantic によるCLIアプリ
- 設計書に沿ったディレクトリ・ファイル構成
- TDD（テスト駆動開発）を推奨
- 型安全・テスト容易性・保守性を重視
- **仮想環境の作成・有効化は不要。`uv run`のみで実行**

---

## 2. 開発環境セットアップ

1. Python 3.9以上をインストール
2. uvをインストール（`pip install uv` または公式手順）
3. 必要パッケージを `pyproject.toml` の `[project.dependencies]` に記載（例: typer, pydantic, pytest, mypy など）
4. コマンドはすべて `uv run todo ...` で実行

---

## 3. 実装ステップ

### ステップ0: プロジェクト初期化
- 設計書通りにディレクトリ・ファイルを作成
- `pyproject.toml` に依存パッケージと `[tool.uv.scripts]` を設定
  ```toml
  [tool.uv.scripts]
  todo = "src/todo.py"
  ```

### ステップ1: データモデルの実装
- `src/models.py` にpydanticでTaskモデルを実装
- モデルのバリデーションテストを`tests/`に作成

### ステップ2: ストレージ層の実装
- `src/storage.py` でtasks.jsonの読み書き関数を実装
- ファイルが存在しない場合の自動生成も実装
- ストレージ層のテストを作成

### ステップ3: CLIコマンドの実装（TDDで各コマンドごとに進める）

#### 3.1 タスク追加
- テストを書く（正常系・異常系）
- `src/commands/add.py` 実装
- `uv run todo add` で動作確認

#### 3.2 タスク一覧表示
- テストを書く（フィルタ・ソート含む）
- `src/commands/list.py` 実装
- `uv run todo list` で動作確認

#### 3.3 タスク完了
- テストを書く
- `src/commands/done.py` 実装
- `uv run todo done <id>` で動作確認

#### 3.4 タスク編集
- テストを書く
- `src/commands/edit.py` 実装
- `uv run todo edit <id>` で動作確認

#### 3.5 タスク削除
- テストを書く
- `src/commands/delete.py` 実装
- `uv run todo delete <id>` で動作確認

### ステップ4: バリデーション・制約の徹底
- 追加・編集時のバリデーションをpydanticで実装
- テストで全バリデーションパターンを網羅

### ステップ5: 統合テスト・カバレッジ向上
- CLI全体の統合テスト
- テストカバレッジ90%以上を目指す

### ステップ6: 型チェック・CI
- mypyで型チェック
- CI（GitHub Actions等）でテスト・型チェック自動化

---

## 4. コマンド実行例

```sh
uv run todo add --name "買い物" --priority "高" --due "2024-06-30"
uv run todo list --priority "高"
uv run todo done 123e4567-e89b-12d3-a456-426614
uv run todo edit 123e4567-e89b-12d3-a456-426614 --name "新しい名前"
uv run todo delete 123e4567-e89b-12d3-a456-426614
```

---

## 5. 注意事項

- **仮想環境の作成・有効化は不要**です。
  `uv run` は `pyproject.toml` の依存を自動的に解決し、グローバル環境を汚さずに実行できます。
- 開発者は `uv run` だけでコマンドを実行・テストできます。
