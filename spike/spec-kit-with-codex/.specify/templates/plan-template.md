# 実装計画: [FEATURE]

**ブランチ**: `[###-feature-name]` | **日付**: [DATE] | **Spec**: [link]
**入力**: `/specs/[###-feature-name]/spec.md` の機能仕様

**注記**: このテンプレートは `/speckit.plan` コマンドで埋められます。実行フローは `.specify/templates/plan-template.md` を参照してください。

## Summary

[機能仕様から抽出: 主要要件 + 調査に基づく技術アプローチ]

## Technical Context

<!--
  ACTION REQUIRED: 以下セクションを、このプロジェクトの技術詳細に置き換えてください。
  構成は反復時のガイドとして提示されています。
-->

**Language/Version**: [例: Python 3.11, Swift 5.9, Rust 1.75 または NEEDS CLARIFICATION]  
**Primary Dependencies**: [例: FastAPI, UIKit, LLVM または NEEDS CLARIFICATION]  
**Storage**: [該当する場合: PostgreSQL, CoreData, files または N/A]  
**Testing**: [例: pytest, XCTest, cargo test または NEEDS CLARIFICATION]  
**Target Platform**: [例: Linux server, iOS 15+, WASM または NEEDS CLARIFICATION]
**Project Type**: [例: library/cli/web-service/mobile-app/compiler/desktop-app または NEEDS CLARIFICATION]  
**Performance Goals**: [領域固有: 例 1000 req/s, 10k lines/sec, 60 fps または NEEDS CLARIFICATION]  
**Constraints**: [領域固有: 例 <200ms p95, <100MB memory, offline-capable または NEEDS CLARIFICATION]  
**Scale/Scope**: [領域固有: 例 10k users, 1M LOC, 50 screens または NEEDS CLARIFICATION]

## Constitution Check

*GATE: Phase 0 の調査前に通過必須。Phase 1 の設計後に再確認。*

[憲章ファイルに基づいて決定されるゲート]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # このファイル (/speckit.plan コマンド出力)
├── research.md          # Phase 0 出力 (/speckit.plan コマンド)
├── data-model.md        # Phase 1 出力 (/speckit.plan コマンド)
├── quickstart.md        # Phase 1 出力 (/speckit.plan コマンド)
├── contracts/           # Phase 1 出力 (/speckit.plan コマンド)
└── tasks.md             # Phase 2 出力 (/speckit.tasks コマンド - /speckit.plan では未作成)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: 下記のプレースホルダーツリーを、この機能の実際の構成へ置き換えてください。
  未使用の選択肢は削除し、選択した構成には実在パス（例: apps/admin, packages/something）を記載してください。
  納品される計画書には Option ラベルを残さないでください。
-->

```text
# [REMOVE IF UNUSED] Option 1: 単一プロジェクト (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web アプリケーション ("frontend" + "backend" を検出した場合)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API ("iOS/Android" を検出した場合)
api/
└── [上記 backend と同様]

ios/ or android/
└── [プラットフォーム固有構成: 機能モジュール, UI フロー, プラットフォームテスト]
```

**Structure Decision**: [選択した構成を記述し、上記で確定した実パスを参照する]

## Complexity Tracking

> **憲章チェックで違反があり、正当化が必要な場合のみ記入**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [例: 4th project] | [現在の必要性] | [3 projects では不足する理由] |
| [例: Repository pattern] | [具体的な問題] | [直接 DB アクセスでは不足する理由] |
