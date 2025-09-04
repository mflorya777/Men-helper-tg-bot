from motor.motor_asyncio import AsyncIOMotorClient


mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["woman_tg_bot"]
users_collection = db["users"]


async def get_user(
    user_id: int,
):
    return await users_collection.find_one(
        {
            "_id": user_id,
        }
    )


async def set_age_confirmed(
    user_id: int,
):
    await users_collection.update_one(
        {
            "_id": user_id,
        },
        {
            "$set": {
                "is_age_confirmed": True,
            },
        },
        upsert=True,
    )
