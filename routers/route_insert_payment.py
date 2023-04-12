from datetime import datetime

from database import db_insert_payment
from fastapi import APIRouter, HTTPException, Request, Response
from schemas import InsertPayment, InsertPaymentBody
from starlette.status import HTTP_201_CREATED
from zaim import zaim_insert_payment

router = APIRouter()


# 支払い登録API
@router.post("/api/v1/money/payment", response_model=InsertPayment)
async def insert_payment(request: Request, response: Response, data: InsertPaymentBody):
    # zaimAPI(create insert/payment)呼び出し
    payment_data = zaim_insert_payment(
        datetime.strptime(data.date, "%Y-%m-%d"),
        data.amount,
        data.genre,
        data.from_account,
    )
    # MongoDBへinsert
    res = await db_insert_payment(payment_data)

    # フロントへレスポンス
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(status_code=404, detail="Create payment failed")
