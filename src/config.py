from os import getenv

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


TOKEN = getenv("BOT_TOKEN")

DEEPSEEK_API_KEY = getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = getenv("DEEPSEEK_API_URL")
MODELS = getenv("MODEL", "").split()

load_dotenv()


class MongoConfig(BaseSettings):
    mongo_user: str | None = None
    mongo_password: str | None = None
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db_name: str = "woman_tg_bot"
    mongo_enable_ssl: bool = False
    mongo_users_collection: str = "users"
