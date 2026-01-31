# タスク管理の実行例

以下はCLIでタスク管理を行う具体例（実行コマンド）です。

## 実行方法（pipenv）
```
pipenv run python -m todo_cli.cli --help
```

## 例1: 追加 → 一覧 → 完了
```
pipenv run python -m todo_cli.cli add "Write spec" --priority high --due 2026-02-05 --category work
pipenv run python -m todo_cli.cli list --sort due
pipenv run python -m todo_cli.cli done <id>
pipenv run python -m todo_cli.cli list --status done
```

## 例2: 優先度とカテゴリで絞り込み
```
pipenv run python -m todo_cli.cli list --priority high --category work
```

## 例3: 期限切れを確認
```
pipenv run python -m todo_cli.cli list --overdue
```

## 例4: タスク編集
```
pipenv run python -m todo_cli.cli edit <id> --title "Prepare slides" --due 2026-02-10 --priority medium
```

## 例5: 検索
```
pipenv run python -m todo_cli.cli search "meeting"
```

## 例6: 完了取り消し
```
pipenv run python -m todo_cli.cli undo <id>
```

## 例7: 削除
```
pipenv run python -m todo_cli.cli delete <id>
```
