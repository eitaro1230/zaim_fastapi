import motor.motor_asyncio
from decouple import config

MONGO_DB_URI = config("MONGO_DB_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)

database = client.zaim_fastapi_db
collection_payment = database.payment


# MongoDBからのレスポンスをdict変換する
def payment_serializer(payment) -> dict:
    return {
        "id": str(payment["_id"]),
        "payment_id": payment["payment_id"],
        "genre": payment["genre"],
        "amount": payment["amount"],
        "date": payment["date"],
        "from_account": payment["from_account"],
    }


# collection payment へ insert する
async def db_insert_payment(data: dict) -> dict | bool:
    payment = await collection_payment.insert_one(data)
    new_payment = await collection_payment.find_one(
        {"_id": payment.inserted_id}
    )
    if new_payment:
        return payment_serializer(new_payment)
    return False
