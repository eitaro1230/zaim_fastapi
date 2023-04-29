from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, Response
from schemas import InsertPaymentBody
from starlette.status import HTTP_201_CREATED
from zaim import api

router = APIRouter()


# 支払い登録API
@router.post("/api/v1/money/payment", response_model=InsertPaymentBody)
def insert_payment(request: Request, response: Response, data: InsertPaymentBody):
    # zaimAPI(create insert/payment)呼び出し
    res = api.insert_payment_simple(
        datetime.strptime(data.date, "%Y-%m-%d"),
        data.amount,
        data.genre,
        data.from_account,
    )

    # フロントへレスポンス
    response.status_code = HTTP_201_CREATED
    if res.status_code == 200:
        return data
    raise HTTPException(status_code=404, detail="Create payment failed")
