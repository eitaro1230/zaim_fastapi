# シーケンス図

```mermaid
sequenceDiagram
    autonumber
    actor person as 人物
    participant line as LINE画面
    participant frontend as フォーム画面
    participant backend as バックエンドAPI
    participant zaim as zaimAPI
    person ->> line:アプリ起動
    line ->> frontend :リンククリック
    Note over frontend:支払情報入力
    frontend ->> backend:支払い情報送信
    Note right of frontend:date<br>amount<br>genre<br>from_account
    backend ->> zaim:POST api/v1/money/payment
    Note right of backend:date<br>amount<br>genre<br>from_account
    zaim ->> backend:response
    Note left of zaim:id
    backend ->> frontend:支払情報登録結果
    Note left of backend:date<br>amount<br>genre<br>from_account
    Note over frontend:画面閉じる
    frontend ->> line:遷移
    line ->> person:アプリ終了
```
