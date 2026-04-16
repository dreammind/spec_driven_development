# Tasks: CLI版TODOタスク管理

**Input**: `/specs/001-cli-todo-app/` の設計ドキュメント  
**Prerequisites**: plan.md（必須）, spec.md（必須）, research.md, data-model.md, contracts/, quickstart.md

**Tests**: 本機能はTDD方針と品質ゲート（カバレッジ90%以上, mypyエラー0件）を要求するため、各ストーリーでテストタスクを含める。  
**Organization**: 各タスクはユーザーストーリー単位でグループ化し、独立実装と独立テストを可能にする。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並列実行可能（別ファイルで依存なし）
- **[Story]**: 対応するユーザーストーリー（例: US1, US2, US3）
- すべてのタスクに実ファイルパスを含める

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Python + uv + pydantic + pytest + mypy の実装基盤を初期化する

- [ ] T001 `pyproject.toml` に `pydantic`, `pytest`, `pytest-cov`, `mypy` を含む依存関係と実行設定を定義する
- [ ] T002 `src/todo_cli/__init__.py`, `src/todo_cli/cli.py`, `src/todo_cli/app.py`, `src/todo_cli/models.py`, `src/todo_cli/repository.py` を作成する
- [ ] T003 `tests/unit/test_models.py`, `tests/unit/test_repository.py`, `tests/integration/test_cli_workflows.py`, `tests/contract/test_cli_contract.py` を作成する
- [ ] T004 `mypy.ini` に `src` と `tests` を対象とした型チェック設定を作成する

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 全ユーザーストーリーに共通のドメイン・永続化・CLI基盤を整備する

**⚠️ CRITICAL**: このフェーズ完了までユーザーストーリー作業を開始しない

- [ ] T005 `src/todo_cli/models.py` に `Task` と `TaskCollection` の `pydantic.BaseModel` 骨組みを作成する
- [ ] T006 `src/todo_cli/repository.py` に JSON ファイル読み書きと永続化境界（load/save）を実装する
- [ ] T007 `src/todo_cli/app.py` にユースケース呼び出し用のアプリケーションサービス骨組みを作成する
- [ ] T008 `src/todo_cli/cli.py` に `argparse` ベースのサブコマンドルーティングと終了コード制御を実装する
- [ ] T009 [P] `tests/conftest.py` に一時ファイルストレージとCLI実行ヘルパーfixtureを追加する

**Checkpoint**: 基盤準備完了。以降、ユーザーストーリー実装を開始可能

---

## Phase 3: User Story 1 - タスクを記録する (Priority: P1) 🎯 MVP

**Goal**: ユーザーがタスクを追加し、既定一覧（未完了のみ）で確認できるようにする

**Independent Test**: `todo add` 後に `todo list` を実行し、新規タスクが未完了一覧に表示されることを確認する

### Tests for User Story 1

- [ ] T010 [P] [US1] `tests/contract/test_cli_contract.py` に `todo add`/`todo list` の契約テストと空タイトル失敗テストを追加する
- [ ] T011 [P] [US1] `tests/integration/test_cli_workflows.py` に追加→一覧表示の統合テストを追加する
- [ ] T012 [P] [US1] `tests/unit/test_models.py` にUUID生成・タイトルバリデーションの単体テストを追加する

### Implementation for User Story 1

- [ ] T013 [US1] `src/todo_cli/models.py` にタイトルtrim/最小文字数・作成日時・UUIDの検証ロジックを実装する
- [ ] T014 [US1] `src/todo_cli/repository.py` にタスク追加と既定一覧（未完了かつ非アーカイブ）取得を実装する
- [ ] T015 [US1] `src/todo_cli/app.py` に `add_task` と `list_tasks` ユースケースを実装する
- [ ] T016 [US1] `src/todo_cli/cli.py` に `todo add` と `todo list` コマンドを実装する
- [ ] T017 [US1] `src/todo_cli/cli.py` に空状態メッセージと入力エラーメッセージを実装する

**Checkpoint**: User Story 1 が単独で動作し、MVPとしてデモ可能

---

## Phase 4: User Story 2 - タスク状態を更新する (Priority: P2)

**Goal**: ユーザーがタスクを完了/未完了に切り替え、必要に応じて完了済みを含む一覧を確認できるようにする

**Independent Test**: タスクを完了化・未完了化したとき、一覧状態が期待どおり変化することを確認する

### Tests for User Story 2

- [ ] T018 [P] [US2] `tests/contract/test_cli_contract.py` に `todo complete`/`todo reopen`/`todo list --all-active` の契約テストを追加する
- [ ] T019 [P] [US2] `tests/integration/test_cli_workflows.py` に完了化→未完了化の統合テストを追加する
- [ ] T020 [P] [US2] `tests/unit/test_repository.py` に未存在ID・不正IDの更新失敗テストを追加する

### Implementation for User Story 2

- [ ] T021 [US2] `src/todo_cli/repository.py` に完了化・未完了化・未アーカイブ全件取得を実装する
- [ ] T022 [US2] `src/todo_cli/app.py` に `complete_task`, `reopen_task`, `list_all_active_tasks` ユースケースを実装する
- [ ] T023 [US2] `src/todo_cli/cli.py` に `todo complete`, `todo reopen`, `todo list --all-active` を実装する
- [ ] T024 [US2] `src/todo_cli/cli.py` にID不正/未存在時の終了コード `2` とエラーメッセージ処理を実装する

**Checkpoint**: User Story 2 がUser Story 1に依存せず独立検証可能

---

## Phase 5: User Story 3 - タスクを整理する (Priority: P3)

**Goal**: ユーザーがタスクをアーカイブ/復元し、復元時に常に未完了へ戻せるようにする

**Independent Test**: アーカイブ後に既定一覧から非表示になり、復元後に未完了で再表示されることを確認する

### Tests for User Story 3

- [ ] T025 [P] [US3] `tests/contract/test_cli_contract.py` に `todo archive`/`todo restore` の契約テストを追加する
- [ ] T026 [P] [US3] `tests/integration/test_cli_workflows.py` にアーカイブ非表示・復元再表示の統合テストを追加する
- [ ] T027 [P] [US3] `tests/unit/test_repository.py` に再アーカイブ失敗と非アーカイブ復元失敗の単体テストを追加する

### Implementation for User Story 3

- [ ] T028 [US3] `src/todo_cli/repository.py` にアーカイブ/復元状態遷移（復元時は常に未完了）を実装する
- [ ] T029 [US3] `src/todo_cli/app.py` に `archive_task` と `restore_task` ユースケースを実装する
- [ ] T030 [US3] `src/todo_cli/cli.py` に `todo archive` と `todo restore` コマンドを実装する
- [ ] T031 [US3] `src/todo_cli/models.py` に復元時完了状態リセットのドメイン制約を実装する

**Checkpoint**: 全ユーザーストーリーが独立して動作し、状態遷移要件を満たす

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 横断品質（型安全性・カバレッジ・ドキュメント）を仕上げる

- [ ] T032 [P] `tests/unit/test_models.py` と `tests/unit/test_repository.py` に境界条件テストを追加しカバレッジ90%以上を達成する
- [ ] T033 `src/todo_cli/models.py`, `src/todo_cli/app.py`, `src/todo_cli/repository.py`, `src/todo_cli/cli.py` の型注釈を補完して `mypy` エラーを解消する
- [ ] T034 [P] `specs/001-cli-todo-app/quickstart.md` に最終コマンドと検証手順を反映する
- [ ] T035 `pyproject.toml` に `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90` と `uv run mypy src tests` の品質ゲート実行手順を明記する

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 依存なし
- **Phase 2 (Foundational)**: Phase 1 完了後に開始（全ストーリーの前提）
- **Phase 3 (US1)**: Phase 2 完了後に開始
- **Phase 4 (US2)**: Phase 2 完了後に開始（US1完了後の順次実行を推奨）
- **Phase 5 (US3)**: Phase 2 完了後に開始（US2完了後の順次実行を推奨）
- **Phase 6 (Polish)**: US1〜US3完了後に実施

### User Story Dependencies

- **US1 (P1)**: 依存なし（MVP）
- **US2 (P2)**: US1 のタスク存在を前提にするが、実装作業はFoundational完了後に開始可能
- **US3 (P3)**: US1/US2 の基盤を利用するが、ストーリーとしては独立検証可能

### Within Each User Story

- テストタスクを先に実装し、失敗を確認してから実装タスクへ進む
- `models.py` → `repository.py` → `app.py` → `cli.py` の順で実装する
- ストーリーごとに完了判定を行ってから次へ進む

### Parallel Opportunities

- Phase 1: T004 は T001-T003 と並列可能
- Phase 2: T009 は T005-T008 と並列可能
- US1: T010-T012 は並列可能
- US2: T018-T020 は並列可能
- US3: T025-T027 は並列可能
- Polish: T032 と T034 は並列可能

---

## Parallel Example: User Story 2

```bash
# 並列で先にテストを作成
Task: "Add contract tests in tests/contract/test_cli_contract.py"
Task: "Add integration tests in tests/integration/test_cli_workflows.py"
Task: "Add unit tests in tests/unit/test_repository.py"

# 実装は依存順で進行
Task: "Implement transition methods in src/todo_cli/repository.py"
Task: "Implement use cases in src/todo_cli/app.py"
Task: "Implement CLI handlers in src/todo_cli/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 と Phase 2 を完了
2. Phase 3 (US1) のみ実装
3. `uv run pytest -q` でUS1シナリオを確認
4. MVPとして共有後にUS2/US3へ進む

### Incremental Delivery

1. US1完了後にデモ
2. US2を追加して状態更新機能をデモ
3. US3を追加してアーカイブ/復元をデモ
4. 最後にPhase 6で横断品質を固定

### Parallel Team Strategy

1. 1名がFoundational（T005-T008）を進行
2. 1名がテスト基盤（T009 と各USのテスト）を進行
3. Foundational完了後、USごとに担当分割して並列実装

---

## Notes

- すべてのタスクはチェックリスト形式・ID・ファイルパス付きで定義済み
- [P] タスクは依存関係がないファイルに限定
- 各ユーザーストーリーは独立テスト可能な粒度で分割済み
