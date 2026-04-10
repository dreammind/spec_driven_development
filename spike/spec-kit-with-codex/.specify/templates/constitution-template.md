# [PROJECT_NAME] 憲章
<!-- 例: Spec Constitution, TaskFlow Constitution など -->

## コア原則

### [PRINCIPLE_1_NAME]
<!-- 例: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- 例: すべての機能は独立ライブラリから開始する。ライブラリは自己完結・独立テスト可能・文書化されていること。組織上の都合だけのライブラリは不可。 -->

### [PRINCIPLE_2_NAME]
<!-- 例: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- 例: 各ライブラリは CLI 経由で機能を公開する。標準入出力プロトコル: stdin/args -> stdout、エラーは stderr。JSON と人間可読形式をサポート。 -->

### [PRINCIPLE_3_NAME]
<!-- 例: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- 例: TDD 必須: テスト作成 -> ユーザー承認 -> テスト失敗確認 -> 実装。Red-Green-Refactor を厳守。 -->

### [PRINCIPLE_4_NAME]
<!-- 例: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- 例: 統合テストが必要な領域: 新規ライブラリの契約テスト、契約変更、サービス間通信、共有スキーマ。 -->

### [PRINCIPLE_5_NAME]
<!-- 例: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- 例: テキストI/Oでデバッグ容易性を確保。構造化ログ必須。あるいは MAJOR.MINOR.BUILD 版管理。あるいは YAGNI を重視した単純設計。 -->

## [SECTION_2_NAME]
<!-- 例: Additional Constraints, Security Requirements, Performance Standards など -->

[SECTION_2_CONTENT]
<!-- 例: 技術スタック要件、コンプライアンス基準、デプロイ方針など -->

## [SECTION_3_NAME]
<!-- 例: Development Workflow, Review Process, Quality Gates など -->

[SECTION_3_CONTENT]
<!-- 例: コードレビュー要件、テストゲート、デプロイ承認プロセスなど -->

## Governance
<!-- 例: 憲章は他の実務ルールに優先。改定には文書化・承認・移行計画が必要 -->

[GOVERNANCE_RULES]
<!-- 例: 全PR/レビューで準拠確認必須。複雑性は正当化必須。実行時開発ガイドとして [GUIDANCE_FILE] を参照。 -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- 例: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
