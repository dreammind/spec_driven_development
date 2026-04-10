---

description: "機能実装のためのタスクリストテンプレート"
---

# Tasks: [FEATURE NAME]

**Input**: `/specs/[###-feature-name]/` の設計ドキュメント  
**Prerequisites**: plan.md（必須）, spec.md（ユーザーストーリーのため必須）, research.md, data-model.md, contracts/

**Tests**: 下記のテストタスクは例です。テストは任意であり、機能仕様で明示的に要求された場合のみ含めてください。

**Organization**: 各タスクはユーザーストーリー単位でグループ化し、独立実装と独立テストを可能にします。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並列実行可能（別ファイルで依存なし）
- **[Story]**: 対応するユーザーストーリー（例: US1, US2, US3）
- 説明には正確なファイルパスを含める

## Path Conventions

- **Single project**: ルートに `src/`, `tests/`
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` または `android/src/`
- 下記のパス例は単一プロジェクト前提です。`plan.md` の構成に合わせて調整してください

<!--
  ============================================================================
  IMPORTANT: 以下のタスクは説明用サンプルです。

  /speckit.tasks コマンドは、次を根拠に必ず実タスクへ置き換えてください:
  - spec.md のユーザーストーリー（P1, P2, P3...）
  - plan.md の機能要件
  - data-model.md のエンティティ
  - contracts/ のエンドポイント

  タスクはユーザーストーリー単位で整理し、各ストーリーが次を満たすこと:
  - 独立して実装できる
  - 独立してテストできる
  - MVP の増分として提供できる

  生成される tasks.md に、このサンプルタスクを残してはいけません。
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: プロジェクト初期化と基本構成

- [ ] T001 実装計画に従ってプロジェクト構造を作成
- [ ] T002 [language] プロジェクトを [framework] 依存で初期化
- [ ] T003 [P] lint/format ツールを設定

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: すべてのユーザーストーリー実装前に完了必須の基盤

**⚠️ CRITICAL**: このフェーズ完了までユーザーストーリー作業を開始しない

基盤タスクの例（プロジェクトに合わせて調整）:

- [ ] T004 DB スキーマとマイグレーション基盤を構築
- [ ] T005 [P] 認証/認可基盤を実装
- [ ] T006 [P] API ルーティングとミドルウェアを設定
- [ ] T007 全ストーリーで共有するベースモデル/エンティティを作成
- [ ] T008 エラーハンドリングとロギング基盤を設定
- [ ] T009 環境設定管理を構築

**Checkpoint**: 基盤準備完了。以降、ユーザーストーリー実装を並列開始可能

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [このストーリーで提供する価値の要約]

**Independent Test**: [このストーリー単独での検証方法]

### Tests for User Story 1 (任意 - テスト要求時のみ) ⚠️

> **NOTE: 先にこれらのテストを書き、実装前に失敗することを確認する**

- [ ] T010 [P] [US1] tests/contract/test_[name].py に [endpoint] の契約テストを追加
- [ ] T011 [P] [US1] tests/integration/test_[name].py に [user journey] の統合テストを追加

### Implementation for User Story 1

- [ ] T012 [P] [US1] src/models/[entity1].py に [Entity1] モデル作成
- [ ] T013 [P] [US1] src/models/[entity2].py に [Entity2] モデル作成
- [ ] T014 [US1] src/services/[service].py に [Service] 実装（T012, T013 依存）
- [ ] T015 [US1] src/[location]/[file].py に [endpoint/feature] 実装
- [ ] T016 [US1] バリデーションとエラー処理を追加
- [ ] T017 [US1] ユーザーストーリー1の処理ログを追加

**Checkpoint**: この時点で User Story 1 は独立して完全動作・検証可能であること

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [このストーリーで提供する価値の要約]

**Independent Test**: [このストーリー単独での検証方法]

### Tests for User Story 2 (任意 - テスト要求時のみ) ⚠️

- [ ] T018 [P] [US2] tests/contract/test_[name].py に [endpoint] の契約テストを追加
- [ ] T019 [P] [US2] tests/integration/test_[name].py に [user journey] の統合テストを追加

### Implementation for User Story 2

- [ ] T020 [P] [US2] src/models/[entity].py に [Entity] モデル作成
- [ ] T021 [US2] src/services/[service].py に [Service] 実装
- [ ] T022 [US2] src/[location]/[file].py に [endpoint/feature] 実装
- [ ] T023 [US2] 必要に応じて User Story 1 コンポーネントと統合

**Checkpoint**: この時点で User Story 1 と 2 の双方が独立動作すること

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [このストーリーで提供する価値の要約]

**Independent Test**: [このストーリー単独での検証方法]

### Tests for User Story 3 (任意 - テスト要求時のみ) ⚠️

- [ ] T024 [P] [US3] tests/contract/test_[name].py に [endpoint] の契約テストを追加
- [ ] T025 [P] [US3] tests/integration/test_[name].py に [user journey] の統合テストを追加

### Implementation for User Story 3

- [ ] T026 [P] [US3] src/models/[entity].py に [Entity] モデル作成
- [ ] T027 [US3] src/services/[service].py に [Service] 実装
- [ ] T028 [US3] src/[location]/[file].py に [endpoint/feature] 実装

**Checkpoint**: すべてのユーザーストーリーが独立して機能すること

---

[必要に応じて、同様のパターンでフェーズを追加]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: 複数ストーリーにまたがる改善

- [ ] TXXX [P] docs/ のドキュメント更新
- [ ] TXXX コード整理とリファクタ
- [ ] TXXX 全ストーリー横断の性能最適化
- [ ] TXXX [P] tests/unit/ に追加ユニットテスト（要求時）
- [ ] TXXX セキュリティ強化
- [ ] TXXX quickstart.md の検証実行

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 依存なし。即開始可能
- **Foundational (Phase 2)**: Setup 完了に依存。全ストーリーをブロック
- **User Stories (Phase 3+)**: すべて Foundational 完了に依存
  - 体制があれば並列実行可能
  - または優先順（P1 → P2 → P3）で順次実行
- **Polish (Final Phase)**: 対象ストーリー完了後に実施

### User Story Dependencies

- **User Story 1 (P1)**: Foundational 後に開始可能。他ストーリー依存なし
- **User Story 2 (P2)**: Foundational 後に開始可能。US1 と統合する場合あり
- **User Story 3 (P3)**: Foundational 後に開始可能。US1/US2 と統合する場合あり

### Within Each User Story

- テストを含める場合、実装前に作成し FAIL を確認する
- モデル → サービス → エンドポイントの順で進める
- 中核実装の後に統合を行う
- 次の優先度へ進む前に当該ストーリーを完了する

### Parallel Opportunities

- Setup の [P] タスクは並列実行可能
- Foundational の [P] タスクもフェーズ内で並列実行可能
- Foundational 完了後は、体制次第で各ストーリーを並列開始可能
- ストーリー内の [P] テストは並列実行可能
- ストーリー内の [P] モデル作成は並列実行可能
- チーム分担により異なるストーリーを並列実装可能

---

## Parallel Example: User Story 1

```bash
# User Story 1 のテストを同時に開始（テスト要求時）:
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# User Story 1 のモデルを同時に開始:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup を完了
2. Phase 2: Foundational を完了（CRITICAL）
3. Phase 3: User Story 1 を完了
4. **STOP and VALIDATE**: User Story 1 を独立検証
5. 準備できていればデプロイ/デモ

### Incremental Delivery

1. Setup + Foundational を完了 → 基盤準備完了
2. User Story 1 追加 → 独立テスト → デプロイ/デモ（MVP）
3. User Story 2 追加 → 独立テスト → デプロイ/デモ
4. User Story 3 追加 → 独立テスト → デプロイ/デモ
5. 各ストーリーは既存を壊さず価値を追加

### Parallel Team Strategy

複数開発者がいる場合:

1. Setup + Foundational をチームで完了
2. Foundational 完了後:
   - 開発者 A: User Story 1
   - 開発者 B: User Story 2
   - 開発者 C: User Story 3
3. 各ストーリーを独立実装し統合

---

## Notes

- [P] タスク = 別ファイル・依存なし
- [Story] ラベルでタスクとストーリーをトレース可能にする
- 各ストーリーは独立して完了・検証可能であること
- 実装前にテスト FAIL を確認する
- 各タスクまたは論理単位ごとにコミットする
- 各チェックポイントで独立検証して進める
- 避けること: 曖昧なタスク、同一ファイル競合、独立性を壊すクロスストーリー依存
