import logging
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import MongoConfig


_LOG = logging.getLogger("woman-tg-bot")


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
        user_id: int,
    ):
        return await self.users_collection.find_one(
            {
                "_id": user_id,
            }
        )

    async def set_age_confirmed(
        self,
        user_id: int,
    ):
        await self.users_collection.update_one(
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
