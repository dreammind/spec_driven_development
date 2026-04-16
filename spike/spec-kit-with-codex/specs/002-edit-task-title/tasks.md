# Tasks: タスクタイトル編集機能

**Input**: `/specs/002-edit-task-title/` の設計ドキュメント  
**Prerequisites**: plan.md（必須）, spec.md（必須）, research.md, data-model.md, contracts/cli-edit-contract.md, quickstart.md

**Tests**: 本機能は TDD 前提のため、各ユーザーストーリーで先に失敗するテストを追加してから実装する。  
**Organization**: タスクはユーザーストーリー単位で分割し、各ストーリーを独立実装・独立検証できる構成にする。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 編集機能追加の前提を整える

- [ ] T001 `pyproject.toml` の開発依存（pytest-cov, mypy）と `mypy.ini` の設定を確認し、不足があれば更新する
- [ ] T002 `specs/002-edit-task-title/contracts/cli-edit-contract.md` と `src/todo_cli/cli.py` の現行CLI差分を洗い出し、対応方針を `specs/002-edit-task-title/plan.md` に追記する

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: すべてのユーザーストーリーで共通利用する編集基盤を先に整備する

**⚠️ CRITICAL**: このフェーズ完了までユーザーストーリー作業を開始しない

- [ ] T003 `src/todo_cli/models.py` にタイトル編集用バリデーション（trim後1〜255文字）と共通定数を追加する
- [ ] T004 [P] `src/todo_cli/repository.py` にタイトル更新の永続化処理（対象ID探索、アーカイブ済み拒否、失敗時非更新）を追加する
- [ ] T005 [P] `src/todo_cli/app.py` に編集ユースケースとドメインエラー（未存在・不正入力・編集不可）を追加する
- [ ] T006 `src/todo_cli/cli.py` に `edit` サブコマンドの骨格（引数受理とアプリ呼び出し）を追加する

**Checkpoint**: 編集機能の土台が揃い、各ストーリーのテスト駆動実装を開始できる

---

## Phase 3: User Story 1 - タイトルを編集する (Priority: P1) 🎯 MVP

**Goal**: 既存タスク1件のタイトルを指定IDで更新できるようにする

**Independent Test**: タスク作成後に `edit --id <uuid> --title <new>` を実行し、同一IDタスクのタイトルだけが更新されることを確認する

### Tests for User Story 1

- [ ] T007 [P] [US1] `tests/contract/test_cli_contract.py` に `todo edit` 成功時の契約テスト（終了コード0、成功メッセージ）を追加する
- [ ] T008 [P] [US1] `tests/integration/test_cli_workflows.py` に単一タスク編集の統合テスト（他タスク不変を含む）を追加する

### Implementation for User Story 1

- [ ] T009 [US1] `src/todo_cli/cli.py` に `todo edit --id --title` の引数処理と成功出力を実装する
- [ ] T010 [US1] `src/todo_cli/app.py` と `src/todo_cli/repository.py` でタイトルのみ更新し、`id/is_completed/is_archived/created_at` を不変に保つ処理を実装する

**Checkpoint**: US1 単体で編集成功フローが動作し、受け入れシナリオ1・2を満たす

---

## Phase 4: User Story 2 - 編集結果を確認する (Priority: P2)

**Goal**: 編集後の一覧表示と再起動後の永続性を確認できるようにする

**Independent Test**: 編集後に `list` を実行し、更新タイトルが表示され、完了状態が維持されることを確認する。再起動後も同様であることを確認する

### Tests for User Story 2

- [ ] T011 [P] [US2] `tests/integration/test_cli_workflows.py` に編集後一覧確認と再起動後保持の統合テストを追加する

### Implementation for User Story 2

- [ ] T012 [US2] `src/todo_cli/repository.py` に編集結果の保存・再読込でタイトルが保持されることを保証する処理を実装する
- [ ] T013 [US2] `src/todo_cli/cli.py` の一覧表示出力で編集後タイトルと既存完了状態が正しく見えることを保証する

**Checkpoint**: US2 単体で「編集→確認」が完了し、SC-001/SC-002の機能要件を満たす

---

## Phase 5: User Story 3 - 不正編集を防ぐ (Priority: P3)

**Goal**: 不正入力・未存在ID・アーカイブ済み編集を拒否し、データを保護する

**Independent Test**: 不正ID、空タイトル、255文字超過、未存在ID、アーカイブ済みIDで `edit` を実行し、終了コード2かつデータ不変を確認する

### Tests for User Story 3

- [ ] T014 [P] [US3] `tests/contract/test_cli_contract.py` に失敗系契約テスト（不正ID/空白/255文字超過/未存在/アーカイブ済み）を追加する
- [ ] T015 [P] [US3] `tests/integration/test_cli_workflows.py` に失敗時データ不変を検証する統合テストを追加する
- [ ] T016 [P] [US3] `tests/unit/test_models.py` にタイトルtrim・長さ制約のユニットテストを追加する
- [ ] T017 [P] [US3] `tests/unit/test_repository.py` にアーカイブ済み拒否と未存在ID時非更新のユニットテストを追加する

### Implementation for User Story 3

- [ ] T018 [US3] `src/todo_cli/models.py` と `src/todo_cli/app.py` に入力検証・エラー分類を実装する
- [ ] T019 [US3] `src/todo_cli/cli.py` に失敗時の人間可読エラー出力と終了コード2へのマッピングを実装する

**Checkpoint**: US3 単体で全不正ケースが安全に拒否され、SC-003 を満たす

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 品質ゲートとドキュメント整合を最終確認する

- [ ] T020 `specs/002-edit-task-title/quickstart.md` の手順で `uv run pytest -q` を実行し、必要に応じて関連テストファイルを修正する
- [ ] T021 `specs/002-edit-task-title/quickstart.md` の手順で `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90` を実行し、カバレッジ不足分を `tests/` 配下に追加する
- [ ] T022 `specs/002-edit-task-title/quickstart.md` の手順で `uv run mypy src tests` を実行し、型エラーを `src/todo_cli/*.py` と `tests/**/*.py` で解消する
- [ ] T023 `specs/002-edit-task-title/spec.md` と `specs/002-edit-task-title/quickstart.md` を更新し、最終受け入れ結果（US1-US3）を反映する

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 依存なし
- **Phase 2 (Foundational)**: Phase 1 完了後に開始
- **Phase 3-5 (User Stories)**: Phase 2 完了後に開始
- **Phase 6 (Polish)**: Phase 3-5 完了後に開始

### User Story Dependencies

- **US1 (P1)**: Foundational 完了後に開始可能（MVP）
- **US2 (P2)**: US1 実装済みの編集機能に依存
- **US3 (P3)**: US1 の編集フローに依存、US2 とは独立で進行可能

### Within Each User Story

- テストタスクを先に実装し、失敗を確認してから実装タスクに進む
- モデル/検証 → アプリユースケース → CLI 出力の順に実装する
- ストーリー完了ごとに独立テストを実施する

### Parallel Opportunities

- Phase 2: T004 と T005 は並列実行可能
- US1: T007 と T008 は並列実行可能
- US3: T014/T015/T016/T017 は並列実行可能
- Phase 6: T021 と T022 は同一ブランチ上で担当分離すれば並列実行可能

---

## Parallel Example: User Story 1

```bash
Task: "T007 [US1] Add contract success test in tests/contract/test_cli_contract.py"
Task: "T008 [US1] Add integration edit workflow test in tests/integration/test_cli_workflows.py"
```

## Parallel Example: User Story 3

```bash
Task: "T014 [US3] Add contract failure tests in tests/contract/test_cli_contract.py"
Task: "T016 [US3] Add model validation unit tests in tests/unit/test_models.py"
Task: "T017 [US3] Add repository invariants tests in tests/unit/test_repository.py"
```

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1-2 を完了して編集基盤を整備する
2. US1（Phase 3）だけを先に完成させる
3. US1 の独立テストを実施して MVP 判定する

### Incremental Delivery

1. US1 完了後に US2 を追加して確認体験を完成させる
2. US3 を追加して不正系防御を完成させる
3. 最後に品質ゲート（mypy・カバレッジ90%以上）を通してリリース可能状態にする
