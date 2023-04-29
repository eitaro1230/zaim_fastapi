from typing import Literal

from pydantic import BaseModel


# def insert_paymentを呼び出すスキーマ
class InsertPaymentBody(BaseModel):
    genre: str
    amount: str
    date: str
    from_account: str


class GetMoneyBody(BaseModel):
    mode: Literal["income", "payment", "transfer"] | None
    start_date: str | None
    end_date: str | None


class SuccessMsg(BaseModel):
    message: str
