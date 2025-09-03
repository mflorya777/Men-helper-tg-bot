from openai import OpenAI


# DEEPSEEK_API_KEY = getenv("DEEPSEEK_API_KEY")
# DEEPSEEK_API_URL = getenv("DEEPSEEK_API_URL")
# MODEL = getenv("MODEL")
DEEPSEEK_API_KEY = "-"
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3.1:free"

CLIENT_DEEPSEEK = OpenAI(
    base_url=DEEPSEEK_API_URL,
    api_key=DEEPSEEK_API_KEY,
)
