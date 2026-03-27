# セッション履歴 — 2026-03-27

## 概要

CLIタスク管理（TODO）アプリをスペックドリブン開発（仕様駆動開発）のアプローチで設計・実装した。

---

## 作成したドキュメント

| ドキュメント | 内容 |
|---|---|
| [doc/Requirement.md](Requirement.md) | 要件定義書 |
| [doc/Design.md](Design.md) | 設計書 |
| [doc/ImplementationPlan.md](ImplementationPlan.md) | TDD実装計画書 |
| [doc/Usage.md](Usage.md) | 一般ユーザー向け利用方法 |

---

## 主な意思決定

### 論理削除の採用
- 当初の設計は物理削除だったが、確認の上**論理削除**に変更
- `Task` モデルに `deleted_at: datetime | None` を追加
- `list` / `show` / `search` では `deleted_at is None` のタスクのみ対象とする

### 検索機能の追加
- 要件定義後に検索機能を追加（タイトルの部分一致検索）
- 要件定義書・設計書・実装計画書・利用方法に反映済み

### 技術スタックの選定
- Python 3.11+ / Typer / Rich / pytest / mypy / uv

---

## 実装結果

| 項目 | 結果 |
|---|---|
| テスト総数 | 72件 |
| テスト結果 | 全パス |
| カバレッジ | 100%（目標90%以上） |
| 型チェック | mypy: no issues |

### 実装ファイル

```
todo_cli/
├── CLAUDE.md
├── .gitignore
├── pyproject.toml
├── src/todo_cli/
│   ├── models.py      # Priority / Task
│   ├── repository.py  # tasks.json 読み書き
│   ├── service.py     # ビジネスロジック
│   ├── display.py     # Rich 表示
│   └── main.py        # Typer CLI（7コマンド）
└── tests/
    ├── test_models.py
    ├── test_repository.py
    ├── test_service.py
    ├── test_display.py
    └── test_main.py
```

---

## 学んだこと・気づき

- ドキュメントに「次の目的」セクションを設けることで、次のステップへの流れが明確になる
- TDDのフロー（テスト失敗 → 実装 → パス）をPhaseごとに守ることで、品質が担保される
- `main.py` のテストは `monkeypatch` でデータファイルパスを差し替えることで、本番データに影響しないテストが書ける
- 新たな機能を追加する場合、新規セッションで実施する方が良いとのこと
  * 理由: 会話が長く続いている。CLAUDE.md を作成済み。ドキュメントが揃っているので、新セッションでも文脈を復元できる
  * 作業ディレクトリを todo_cli/ にした状態で開始し、最初に必要なドキュメントをメンションするとスムーズです。
  * 例) @doc/Design.md @doc/ImplementationPlan.md に基づいて〇〇機能を追加してください

---

## データ保存先

```
~/.todo_cli/tasks.json
```
