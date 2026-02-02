# TODO CLI アプリケーション 利用方法

## はじめに
このドキュメントは、TODO CLIアプリケーションの基本的な使い方を説明します。

## インストール
(ここにアプリケーションのインストール手順を記述します)

## コマンド一覧

### 1. タスクを追加する (`add`)
新しいタスクを追加します。

**コマンド**
```bash
todo add "タスクのタイトル" [OPTIONS]
```

**オプション**
- `--priority INTEGER`: 優先度を1(高)〜5(低)で設定します (デフォルト: 3)。
- `--due-date YYYY-MM-DD`: タスクの期限を設定します。
- `--category TEXT`: タスクのカテゴリを設定します (デフォルト: default)。

**例**
```bash
# シンプルなタスクを追加
todo add "牛乳を買う"

# 優先度と期限付きでタスクを追加
todo add "報告書を提出する" --priority 1 --due-date 2026-03-15
```

### 2. タスクを一覧表示する (`list`)
登録されているタスクを一覧表示します。

**コマンド**
```bash
todo list [OPTIONS]
```

**オプション**
- `--category TEXT`: 指定したカテゴリのタスクのみ表示します。
- `--sort-by TEXT`: 表示順をソートします (`priority`, `due-date`など)。

**例**
```bash
# すべてのタスクを表示
todo list

# '仕事' カテゴリのタスクを優先度順に表示
todo list --category "仕事" --sort-by "priority"
```

### 3. タスクを編集する (`edit`)
既存のタスクの内容を編集します。

**コマンド**
```bash
todo edit TASK_ID [OPTIONS]
```

**引数**
- `TASK_ID`: 編集したいタスクのID。

**オプション**
- `--title TEXT`: 新しいタイトル。
- `--priority INTEGER`: 新しい優先度。
- `--due-date YYYY-MM-DD`: 新しい期限。
- `--category TEXT`: 新しいカテゴリ。

**例**
```bash
# IDが3のタスクの優先度を2に変更
todo edit 3 --priority 2
```

### 4. タスクを完了する (`complete`)
指定したタスクを完了状態にします。

**コマンド**
```bash
todo complete TASK_ID
```

**例**
```bash
# IDが5のタスクを完了にする
todo complete 5
```

### 5. タスクを削除する (`delete`)
指定したタスクを削除します。

**コマンド**
```bash
todo delete TASK_ID
```

**例**
```bash
# IDが2のタスクを削除する
todo delete 2
```

### 6. タスクを検索する (`search`)
キーワードに一致するタスクを検索します。

**コマンド**
```bash
todo search "キーワード"
```

**例**
```bash
# '報告書' という単語が含まれるタスクを検索
todo search "報告書"
```
