from typing import Literal

from decouple import config
from pyzaim import ZaimAPI
from requests_oauthlib import OAuth1Session

api = ZaimAPI(
    consumer_id=config("ZAIM_CONSUMER_ID"),
    consumer_secret=config("ZAIM_CONSUMER_SECRET"),
    access_token=config("ZAIM_ACCESS_TOKEN"),
    access_token_secret=config("ZAIM_ACCESS_TOKEN_SECRET"),
    oauth_verifier=config("ZAIM_VERIFIER"),
)


auth = OAuth1Session(
    client_key=config("ZAIM_CONSUMER_ID"),
    client_secret=config("ZAIM_CONSUMER_SECRET"),
    resource_owner_key=config("ZAIM_ACCESS_TOKEN"),
    resource_owner_secret=config("ZAIM_ACCESS_TOKEN_SECRET"),
    callback_uri="https://www.zaim.net/",
    verifier=config("ZAIM_VERIFIER"),
)


def category_id_to_category_name(category_id: int) -> str:
    """カテゴリーidをカテゴリー名に変換

    Args:
        category_id (int): カテゴリーid

    Returns:
        str: カテゴリー名
    """
    if category_id == 0:
        return ""
    return api.category_itos[category_id]


def genre_id_to_genre_name(genre_id: int) -> str:
    """ジャンルidをジャンル名に変換

    Args:
        genre_id (int): ジャンルid

    Returns:
        str: ジャンル名
    """
    if genre_id == 0:
        return ""
    return api.genre_itos[genre_id]


def account_id_to_account_name(account_id: int) -> str:
    """口座idを口座名に変換

    Args:
        account_id (int): 口座id

    Returns:
        str: 口座名
    """
    if account_id == 0:
        return ""
    return api.account_itos[account_id]


def mode_en_to_mode_ja(
    mode: Literal["income", "payment", "transfer"]
) -> Literal["収入", "支出", "振替"]:
    """記録モード名を日本語変換

    Returns:
        _type_: 記録モード名
    """
    if mode == "income":
        return "収入"
    if mode == "payment":
        return "支出"
    if mode == "transfer":
        return "振替"


def zaim_data_serializer(zaim_data: dict) -> dict:
    """zaimAPIから取得した記録を画面表示用に変換

    Args:
        zaim_data (dict): zaim_get_manual_all_dataのresponse

    Returns:
        dict: 画面表示用の記録データ
    """
    return {
        "id": zaim_data["id"],
        "mode": mode_en_to_mode_ja(zaim_data["mode"]),
        "date": zaim_data["date"],
        "category": category_id_to_category_name(zaim_data["category_id"]),
        "genre": genre_id_to_genre_name(zaim_data["genre_id"]),
        "to_account": account_id_to_account_name(zaim_data["to_account_id"]),
        "from_account": account_id_to_account_name(zaim_data["from_account_id"]),
        "amount": zaim_data["amount"],
    }


def zaim_get_manual_all_data(
    mode: Literal["income", "payment", "transfer"] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict] | bool:
    """zaimAPIから日付を指定して手動記録の履歴を取得

    Args:
        start_date (str): 開始日付
        end_date (str): 終了日付

    Returns:
        list[dict] | bool: 履歴
    """
    params = {}
    if mode:
        params["mode"] = mode
    if start_date:
        params["start_date"] = start_date  # type: ignore
    if end_date:
        params["end_date"] = end_date  # type: ignore
    res = auth.get(url="https://api.zaim.net/v2/home/money", params=params)
    if res.status_code == 200:
        data = res.json()["money"]
        data_list = list(map(zaim_data_serializer, data))
        return data_list
    return False


def zaim_insert_payment(date, amount, genre: str, from_account: str) -> dict | bool:
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
    return False


print(zaim_get_manual_all_data(start_date="2023-04-01"))
