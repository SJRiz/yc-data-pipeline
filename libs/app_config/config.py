import os
from dotenv import load_dotenv
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
LLM_MODEL = os.getenv("LLM_MODEL", "gemma:2b-instruct-q4_K_M")

RETRY_DELAY = 2.5
COMPANIES_PER_EXTRACT = 5
USE_OLLAMA_LOCALLY = True

X_ALGOLIA_API_KEY = os.getenv("x_algolia_api_key")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)