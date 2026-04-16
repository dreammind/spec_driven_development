# Research: CLI版TODOタスク管理

## Decision 1: 実装言語とCLI基盤
- Decision: Python 3.12 + 標準ライブラリ `argparse` を採用する。
- Rationale: CLIの引数検証・ヘルプ表示を標準機能で実現でき、Pydanticと組み合わせた構成でも過剰な複雑化を避けられる。v1の要件規模に対して十分。
- Alternatives considered:
  - Click/Typer: 開発体験は良いが、v1で追加依存を増やす必要性が低い。
  - Go/Rust: 実行バイナリとして強いが、現プロジェクト前提からは初期コストが高い。

## Decision 2: 永続化方式
- Decision: ローカルJSONファイル1つでタスクを永続化する。
- Rationale: 単一ユーザー前提・ローカルCLI要件に適合し、導入/運用が簡単。FR-008の再起動後保持を満たす。
- Alternatives considered:
  - SQLite: 整合性は高いがv1では構成が重い。
  - メモリのみ: 再起動後保持要件を満たせない。

## Decision 3: タスク状態モデル
- Decision: タスクは `is_completed` と `is_archived` を持ち、復元時は必ず `is_completed=false` に戻す。
- Rationale: Clarification結果（削除=アーカイブ、復元時は未完了）を直接表現できる。
- Alternatives considered:
  - 単一ステータス enum: 状態遷移の意図がやや読みにくくなる。
  - 物理削除: 復元要件（FR-010）を満たせない。

## Decision 4: 一覧表示の既定動作
- Decision: 既定は未完了かつ非アーカイブのみ表示し、明示オプションで完了済みを含める。
- Rationale: Clarification結果とFR-003/FR-006に整合し、日常利用で出力ノイズを抑えられる。
- Alternatives considered:
  - 常に全件表示: 利用者が未完了確認しづらい。
  - 完了のみ表示: 主要ユースケースに不一致。

## Decision 5: テスト戦略
- Decision: pytestで unit / integration / contract の3層テストを実施する。
- Rationale: 憲章のTDD方針とトレーサビリティ要件に合致し、状態遷移・永続化・CLI挙動を分離検証できる。加えてカバレッジ90%以上を品質目標として管理する。
- Alternatives considered:
  - 手動テスト中心: 回帰リスクが高い。
  - unitのみ: CLI契約と統合挙動を十分に保証できない。

## Decision 6: Python環境・依存管理
- Decision: Python実行と依存管理は `uv` を使用する（`uv sync`, `uv run`）。
- Rationale: ローカル開発で再現性の高い環境管理ができ、実行コマンドを統一できる。
- Alternatives considered:
  - venv + pip: 一般的だが、プロジェクトごとの実行統一が弱い。
  - poetry: 高機能だがv1要件に対しては運用が重い。

## Decision 7: 型安全性の担保
- Decision: 静的型チェックに `mypy` を採用し、`uv run mypy src tests` を必須チェックとする。
- Rationale: 実装初期から型不整合を検出でき、リファクタリング時の回帰リスクを下げられる。
- Alternatives considered:
  - 型チェックなし: 実行時まで不整合を検出できない。
  - pyright: 高速だが、v1では既存のpytest中心フローにmypy統合が簡潔。

## Decision 8: データ検証と型管理
- Decision: ドメインデータモデルは `pydantic` で定義し、入力・永続化復元時の検証を一元化する。
- Rationale: バリデーションロジックの散在を防ぎ、モデル定義と検証ルールを同じ場所で管理できる。
- Alternatives considered:
  - dataclass + 手動検証: 検証漏れが起きやすい。
  - attrs: 選択肢として有効だが、型ヒントとバリデーション統合でpydanticの方が導入しやすい。
