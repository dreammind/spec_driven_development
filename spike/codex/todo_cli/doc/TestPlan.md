# テスト項目一覧

## 1. add（追加）
- 正常系: 必須項目のみで追加できる
- 正常系: description / due_date / categories を含めて追加できる
- 正常系: categories を複数指定できる
- 異常系: title が空文字の場合エラー
- 異常系: priority が不正値の場合エラー
- 異常系: due_date が不正形式の場合エラー

## 2. list（一覧）
- 正常系: すべてのタスクを表示できる
- 正常系: status=open で未完了のみ表示
- 正常系: status=done で完了のみ表示
- 正常系: priority フィルタが動作する
- 正常系: category フィルタが動作する
- 正常系: sort=due が期限順で表示される
- 正常系: sort=priority が優先度順で表示される
- 正常系: sort=created が作成順で表示される
- 正常系: overdue オプションで期限切れのみ表示

## 3. done（完了）
- 正常系: 指定IDのタスクを完了にできる
- 正常系: completed_at が設定される
- 異常系: 存在しないIDはエラー

## 4. undo（取り消し）
- 正常系: 完了済みタスクを未完了に戻せる
- 正常系: completed_at が null に戻る
- 異常系: 存在しないIDはエラー

## 5. delete（削除）
- 正常系: 指定IDのタスクを削除できる
- 異常系: 存在しないIDはエラー

## 6. edit（編集）
- 正常系: title を更新できる
- 正常系: description を更新できる
- 正常系: priority を更新できる
- 正常系: due_date を更新できる
- 正常系: categories を更新できる
- 異常系: title が空文字の場合エラー
- 異常系: priority が不正値の場合エラー
- 異常系: due_date が不正形式の場合エラー

## 7. search（検索）
- 正常系: title に一致するタスクが見つかる
- 正常系: description に一致するタスクが見つかる
- 正常系: 部分一致ができる

## 8. ストレージI/O
- 正常系: tasks.json が存在しない場合は空として扱う
- 異常系: JSON/YAMLが壊れている場合はエラー
- 正常系: 保存後に再読み込みできる

## 9. 境界値・例外
- タイトルが長文でも追加できる
- description が空でも追加できる
- categories が空配列の場合でも追加できる
- due_date が過去日付でも追加できる

