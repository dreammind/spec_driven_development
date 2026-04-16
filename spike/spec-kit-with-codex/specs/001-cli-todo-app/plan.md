# 実装計画: CLI版TODOタスク管理

**ブランチ**: `001-cli-todo-app` | **日付**: 2026-04-16 | **Spec**: [/Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex/specs/001-cli-todo-app/spec.md](/Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex/specs/001-cli-todo-app/spec.md)
**入力**: `/specs/001-cli-todo-app/spec.md` の機能仕様

## Summary

CLIベースのTODOアプリを、単一ローカルユーザー向けに実装する。v1では「追加・一覧（既定は未完了のみ）・完了化/未完了化・アーカイブ・復元」を対象とし、タスクIDはUUIDを採用する。永続化はローカルファイルで行い、Pydanticでデータ検証と型管理を行う。標準入出力の明確なメッセージ設計と、TDDベースの自動テストで受け入れ条件を担保する。

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Python標準ライブラリ（argparse, uuid, json, pathlib, datetime）, pydantic, uv, pytest, mypy  
**Storage**: ローカルJSONファイル（単一ファイル永続化）  
**Testing**: uv run pytest（unit + integration + contract）, uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90, uv run mypy src tests  
**Target Platform**: macOS / Linux のターミナル環境  
**Project Type**: cli  
**Performance Goals**: 有効コマンドの95%以上で2秒以内に応答（SC-002）  
**Constraints**: 単一ローカルユーザー、オフライン動作、復元時は常に未完了へ戻す、Pydantic検証エラーを適切にユーザー向けメッセージ化する、型チェックエラーゼロを維持する、テストカバレッジ90%以上を維持する  
**Scale/Scope**: 初期想定は1ユーザー・最大1,000タスク程度のローカル運用

## Constitution Check

*GATE: Phase 0 の調査前に通過必須。Phase 1 の設計後に再確認。*

- I. 仕様先行の定義: **PASS**  
  理由: `spec.md` が存在し、Clarificationsで主要曖昧点（ID形式、削除方式、復元時状態、v1スコープ）を解消済み。
- II. ストーリー単位のデリバリー: **PASS**  
  理由: User Story 1/2/3 が独立して価値提供・検証可能。
- III. リスクベースの検証: **PASS**  
  理由: 主要状態遷移とエラー系を unit/integration/contract テストで分離検証し、Pydanticによる入力/データ検証と型チェックを品質ゲートに含める方針。
- IV. トレーサブルな計画: **PASS**  
  理由: FR-001〜FR-010 と設計成果物（data-model / contracts / quickstart）を対応付ける。
- V. 最小で説明可能な変更: **PASS**  
  理由: v1は標準ライブラリ中心の単純構成とし、編集機能は明示的にスコープ外。

**Post-Design Constitution Check**: **PASS**  
Phase 1成果物（`data-model.md`, `contracts/cli-contract.md`, `quickstart.md`）で上記原則との矛盾はなく、過剰な複雑化は発生していない。

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── todo_cli/
│   ├── app.py
│   ├── models.py
│   ├── repository.py
│   └── cli.py
└── lib/

tests/
├── contract/
│   └── test_cli_contract.py
├── integration/
│   └── test_cli_workflows.py
└── unit/
    ├── test_models.py
    └── test_repository.py
```

**Structure Decision**: 単一CLIプロジェクト構成を採用。`src/todo_cli` にドメイン・永続化・CLI入出力を分離し、`tests` は契約/結合/単体で層別化する。

## Complexity Tracking

現時点で憲章違反に該当する複雑化はなし。
