from pydantic import BaseModel


# MongoDBへ格納するスキーマ
class InsertPayment(BaseModel):
    id: str
    payment_id: str
    genre: str
    amount: str
    date: str
    from_account: str


# def insert_paymentを呼び出すスキーマ
class InsertPaymentBody(BaseModel):
    genre: str
    amount: str
    date: str
    from_account: str


class SuccessMsg(BaseModel):
    message: str
