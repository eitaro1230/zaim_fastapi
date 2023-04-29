from decouple import config
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import route_money, route_payment
from schemas import SuccessMsg

app = FastAPI()

origins = [config("ORIGIN")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
)
app.include_router(route_money.router)
app.include_router(route_payment.router)


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welcome to Fast API"}
