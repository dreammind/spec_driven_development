# 利用方法 — CLIタスク管理（TODO）アプリ

## インストール

```bash
# リポジトリをクローン
git clone <リポジトリURL>
cd todo_cli

# 依存パッケージをインストール
uv sync

# コマンドが使えることを確認
todo --help
```

---

## 基本的な使い方

### タスクを追加する

```bash
todo add "タスクのタイトル"
```

優先度・期限・カテゴリを指定することもできます。

```bash
# 優先度を指定（high / medium / low）
todo add "企画書を作成する" --priority high

# 期限を指定（YYYY-MM-DD形式）
todo add "請求書を送る" --due-date 2026-03-31

# カテゴリを指定
todo add "買い物リストを作る" --category 買い物

# すべてを指定
todo add "レポートを提出する" --priority high --due-date 2026-03-31 --category 仕事
```

---

### タスク一覧を表示する

```bash
todo list
```

#### 絞り込み表示

```bash
# 未完了のタスクのみ
todo list --undone

# 完了済みのタスクのみ
todo list --done

# 優先度:高のタスクのみ
todo list --priority high

# カテゴリで絞り込む
todo list --category 仕事

# 期限切れのタスクのみ
todo list --overdue
```

#### 並べ替え

```bash
# 優先度順
todo list --sort priority

# 期限順
todo list --sort due-date

# 作成日順
todo list --sort created-at
```

---

### タスクの詳細を表示する

```bash
todo show <タスクID>
```

例：
```bash
todo show a1b2c3d4
```

---

### タスクを完了にする

```bash
todo done <タスクID>
```

例：
```bash
todo done a1b2c3d4
```

---

### タスクを編集する

変更したい項目だけ指定できます。

```bash
todo edit <タスクID> --title "新しいタイトル"
todo edit <タスクID> --priority low
todo edit <タスクID> --due-date 2026-04-15
todo edit <タスクID> --category プライベート
```

---

### タスクを削除する

```bash
todo delete <タスクID>
```

> 削除したタスクは一覧や検索には表示されなくなります。

---

### タスクを検索する

タイトルに含まれるキーワードで検索します。

```bash
todo search "キーワード"
```

例：
```bash
todo search "レポート"
```

一致するタスクがない場合は「該当するタスクが見つかりませんでした」と表示されます。

---

## コマンド一覧

| コマンド | 説明 |
|---|---|
| `todo add <タイトル>` | タスクを追加する |
| `todo list` | タスク一覧を表示する |
| `todo show <ID>` | タスクの詳細を表示する |
| `todo done <ID>` | タスクを完了にする |
| `todo edit <ID>` | タスクを編集する |
| `todo delete <ID>` | タスクを削除する |
| `todo search <キーワード>` | タイトルでタスクを検索する |

各コマンドの詳細はヘルプで確認できます。

```bash
todo --help
todo add --help
todo list --help
```

---

## データについて

タスクのデータはアプリと同じディレクトリの `tasks.json` に自動的に保存されます。外部サービスには送信されません。
