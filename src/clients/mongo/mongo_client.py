import logging
from typing import Optional
import datetime as dt

from motor.motor_asyncio import AsyncIOMotorClient

from src.config import MongoConfig
from src.models.mongo_models import User


_LOG = logging.getLogger("woman-tg-bot")

MOSCOW_TZ = dt.timezone(dt.timedelta(hours=3))


class MongoClient:
    def __init__(self, config: MongoConfig):
        self.user = config.mongo_user = None
        self.password = config.mongo_password = None
        self.host = config.mongo_host
        self.port = config.mongo_port
        self.db_name = config.mongo_db_name
        self.enable_ssl = config.mongo_enable_ssl
        self.users_collection_name = config.mongo_users_collection

        self.client = self.get_mongo_client()
        self.db = self.client[self.db_name]
        self.users_collection = self.db[self.users_collection_name]

    def get_mongo_client(
        self,
        ) -> AsyncIOMotorClient:
        if self.user and self.password:
            uri = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}"
        else:
            uri = f"mongodb://{self.host}:{self.port}"

        return AsyncIOMotorClient(
            uri,
            tls=self.enable_ssl,
        )

    async def ping(
        self,
    ):
        """
        Infrastructure.
        """
        try:
            await self.client.admin.command(
                "ping",
            )
            _LOG.info(
                "Соединение с MongoDB успешно!"
            )
        except Exception as e:
            _LOG.error(
                e
            )

    async def get_user(
        self,
        tg_user_id: int,
    ) -> Optional[User]:
        doc = await self.users_collection.find_one(
            {
                "id": tg_user_id,
            }
        )
        if not doc:
            return None
        return User(**doc)

    async def set_age_confirmed(
        self,
        user: User,
    ):
        user.is_age_confirmed = True
        now = dt.datetime.now(tz=MOSCOW_TZ)

        if not user.created_at:
            user.created_at = now
        user.updated_at = now

        user_dict = user.dict()

        await self.users_collection.update_one(
            {
                "id": user.id,
            },
            {
                "$set": user_dict,
            },
            upsert=True
        )

    async def update_subscription(
        self,
        user: User,
        has_subscription: bool,
    ) -> None:
        await self.users_collection.update_one(
            {
                "id": user.id,
            },
            {
                "$set": {
                    "has_subscription": has_subscription,
                }
            },
            upsert=True,
        )

    async def update_subscription_expires(
        self,
        user: User,
        subscription_expires_at: dt.datetime,
    ) -> None:
        await self.users_collection.update_one(
            {
                "id": user.id,
            },
            {
                "$set": {
                    "subscription_expires_at": subscription_expires_at,
                }
            },
            upsert=True,
        )
