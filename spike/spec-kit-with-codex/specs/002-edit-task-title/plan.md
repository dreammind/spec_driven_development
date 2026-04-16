# 実装計画: タスクタイトル編集機能

**ブランチ**: `002-edit-task-title` | **日付**: 2026-04-16 | **Spec**: [/Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex/specs/002-edit-task-title/spec.md](/Users/kazu/ws/spec_driven_development/spike/spec-kit-with-codex/specs/002-edit-task-title/spec.md)
**入力**: `/specs/002-edit-task-title/spec.md` の機能仕様

## Summary

既存CLI TODOアプリにタスクタイトル編集機能を追加する。対象は「非アーカイブ/アーカイブ済みを含む既存タスクのうち、アーカイブ済みは編集不可」とし、編集時はタイトルの空白・長さ（最大255文字）を検証する。データモデル・永続化・CLI契約・エラーメッセージを既存仕様と整合させ、TDDと品質ゲート（mypy・カバレッジ90%以上）で回帰を防ぐ。

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: pydantic, uv, pytest, pytest-cov, mypy, Python標準ライブラリ（argparse, json, pathlib, uuid, datetime）  
**Storage**: ローカルJSONファイル（既存タスクストレージ）  
**Testing**: `uv run pytest -q`, `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90`, `uv run mypy src tests`  
**Target Platform**: macOS / Linux ターミナル環境  
**Project Type**: cli  
**Performance Goals**: 有効な編集操作の95%以上を2秒以内に完了（SC-001）  
**Constraints**: 単一ローカルユーザー、オフライン動作、タイトルはtrim後1〜255文字、アーカイブ済み編集は禁止、v1.1で編集履歴保持なし、型チェックエラーゼロを維持、テストカバレッジ90%以上を維持  
**Scale/Scope**: 1ユーザー・最大1,000タスク想定、編集対象はタイトルのみ

## Constitution Check

*GATE: Phase 0 の調査前に通過必須。Phase 1 の設計後に再確認。*

- I. 仕様先行の定義: **PASS**  
  理由: `spec.md` が存在し、clarifyでスコープ（アーカイブ編集不可・255文字上限・履歴なし）が確定済み。
- II. ストーリー単位のデリバリー: **PASS**  
  理由: US1（編集）、US2（確認）、US3（不正系）の独立検証が可能。
- III. リスクベースの検証: **PASS**  
  理由: 単体/統合/契約テストと型検査を実施し、既存機能回帰も確認する方針。
- IV. トレーサブルな計画: **PASS**  
  理由: FR-001〜FR-009 をデータモデル・CLI契約・テスト計画へ直接対応付ける。
- V. 最小で説明可能な変更: **PASS**  
  理由: 既存構造を維持し、編集機能のみを最小差分で追加する。

**Post-Design Constitution Check**: **PASS**  
Phase 1成果物（`data-model.md`, `contracts/cli-edit-contract.md`, `quickstart.md`）は憲章原則と整合し、不要な複雑化は発生していない。

## Project Structure

### Documentation (this feature)

```text
specs/002-edit-task-title/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-edit-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── todo_cli/
    ├── app.py
    ├── cli.py
    ├── models.py
    └── repository.py

tests/
├── contract/
│   └── test_cli_contract.py
├── integration/
│   └── test_cli_workflows.py
└── unit/
    ├── test_models.py
    └── test_repository.py
```

**Structure Decision**: 既存単一CLIプロジェクト構成を維持。編集機能は `repository`（永続化更新）→`app`（ユースケース）→`cli`（入力契約）の順で追加し、既存テスト群に編集シナリオを増分する。

## CLI Contract Alignment

- `contracts/cli-edit-contract.md` の `todo edit --id <uuid> --title <text>` に合わせて `src/todo_cli/cli.py` に `edit` サブコマンドを追加。
- 正常系は終了コード `0` と `edited: <id> | <title>` 出力に統一。
- 契約違反（不正ID、空白タイトル、255文字超過、未存在ID、アーカイブ済み編集）は終了コード `2` に統一。
- 編集成功時は `title` のみ更新し、`id/is_completed/is_archived/created_at` の不変条件を `app/repository` で保証。

## Complexity Tracking

現時点で憲章違反に該当する複雑化はなし。
