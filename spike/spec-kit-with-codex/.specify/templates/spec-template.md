# 機能仕様: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(必須)*

<!--
  IMPORTANT: ユーザーストーリーは重要度順のユーザージャーニーとして優先順位付けしてください。
  各ストーリー/ジャーニーは独立してテスト可能である必要があります。つまり、
  1つだけ実装しても価値ある MVP を提供できることが条件です。

  各ストーリーに優先度 (P1, P2, P3...) を割り当て、P1 を最重要とします。
  各ストーリーを以下を満たす独立スライスとして扱ってください:
  - 独立して開発できる
  - 独立してテストできる
  - 独立してデプロイできる
  - 独立してデモできる
-->

### User Story 1 - [Brief Title] (Priority: P1)

[このユーザージャーニーを平易な言葉で説明]

**Why this priority**: [価値と優先度理由を説明]

**Independent Test**: [独立テスト方法を説明。例: "[specific action] で完全に検証でき、[specific value] を提供する"]

**Acceptance Scenarios**:

1. **Given** [初期状態], **When** [操作], **Then** [期待結果]
2. **Given** [初期状態], **When** [操作], **Then** [期待結果]

---

### User Story 2 - [Brief Title] (Priority: P2)

[このユーザージャーニーを平易な言葉で説明]

**Why this priority**: [価値と優先度理由を説明]

**Independent Test**: [独立テスト方法を説明]

**Acceptance Scenarios**:

1. **Given** [初期状態], **When** [操作], **Then** [期待結果]

---

### User Story 3 - [Brief Title] (Priority: P3)

[このユーザージャーニーを平易な言葉で説明]

**Why this priority**: [価値と優先度理由を説明]

**Independent Test**: [独立テスト方法を説明]

**Acceptance Scenarios**:

1. **Given** [初期状態], **When** [操作], **Then** [期待結果]

---

[必要に応じて、優先度を付けたストーリーを追加]

### Edge Cases

<!--
  ACTION REQUIRED: 以下はプレースホルダーです。適切なエッジケースで置き換えてください。
-->

- [境界条件] のとき何が起こるか？
- [エラーシナリオ] をどのように処理するか？

## Requirements *(必須)*

<!--
  ACTION REQUIRED: 以下はプレースホルダーです。適切な機能要件で置き換えてください。
-->

### Functional Requirements

- **FR-001**: System MUST [具体的な能力。例: "allow users to create accounts"]
- **FR-002**: System MUST [具体的な能力。例: "validate email addresses"]
- **FR-003**: Users MUST be able to [主要操作。例: "reset their password"]
- **FR-004**: System MUST [データ要件。例: "persist user preferences"]
- **FR-005**: System MUST [挙動。例: "log all security events"]

*不明確要件の記載例:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: 認証方式未指定 - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: 保持期間未指定]

### Key Entities *(データが関わる機能の場合に記載)*

- **[Entity 1]**: [何を表すか。実装詳細なしで主要属性を記述]
- **[Entity 2]**: [何を表すか。エンティティ間関係を記述]

## Success Criteria *(必須)*

<!--
  ACTION REQUIRED: 測定可能な成功基準を定義してください。
  技術非依存かつ測定可能である必要があります。
-->

### Measurable Outcomes

- **SC-001**: [測定指標。例: "Users can complete account creation in under 2 minutes"]
- **SC-002**: [測定指標。例: "System handles 1000 concurrent users without degradation"]
- **SC-003**: [ユーザー満足指標。例: "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [ビジネス指標。例: "Reduce support tickets related to [X] by 50%"]

## Assumptions

<!--
  ACTION REQUIRED: 以下はプレースホルダーです。
  機能説明で未指定だった点について、妥当な既定値を前提として記述してください。
-->

- [対象ユーザーに関する前提。例: "Users have stable internet connectivity"]
- [スコープ境界に関する前提。例: "Mobile support is out of scope for v1"]
- [データ/環境に関する前提。例: "Existing authentication system will be reused"]
- [既存システム/サービスへの依存。例: "Requires access to the existing user profile API"]
