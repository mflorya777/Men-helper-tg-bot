from openai import OpenAI

from src.config import (
    DEEPSEEK_API_URL,
    DEEPSEEK_API_KEY,
)


CLIENT_DEEPSEEK = OpenAI(
    base_url=DEEPSEEK_API_URL,
    api_key=DEEPSEEK_API_KEY,
)
