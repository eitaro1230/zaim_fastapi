from decouple import config
from pyzaim import ZaimAPI

api = ZaimAPI(
    consumer_id=config("ZAIM_CONSUMER_ID"),
    consumer_secret=config("ZAIM_CONSUMER_SECRET"),
    access_token=config("ZAIM_ACCESS_TOKEN"),
    access_token_secret=config("ZAIM_ACCESS_TOKEN_SECRET"),
    oauth_verifier=config("ZAIM_VERIFIER"),
)


def zaim_insert_payment(date, amount, genre, from_account):
    # zaimAPI(create insert/payment)呼び出し
    res = api.insert_payment_simple(date, amount, genre, from_account)
    if res.status_code == 200:
        data = res.json()
        # zaimに登録したidのみ抽出(削除する際に指定するidのため)
        payment_id = data["money"]["id"]
        return {
            "payment_id": payment_id,
            "genre": genre,
            "amount": amount,
            "date": str(date),
            "from_account": from_account,
        }
