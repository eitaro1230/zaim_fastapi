from fastapi import FastAPI
from routers import route_insert_payment
from schemas import SuccessMsg

app = FastAPI()
app.include_router(route_insert_payment.router)


@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welcome to Fast API"}
