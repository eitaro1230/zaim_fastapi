from fastapi import APIRouter, HTTPException, Request, Response

# from schemas import GetMoneyBody
from zaim import zaim_get_manual_all_data

router = APIRouter()


@router.get("/api/v1/money")
def get_money(request: Request, response: Response):
    data = zaim_get_manual_all_data()
    if data:
        return data
    raise HTTPException(status_code=404, detail="Get money failed")
