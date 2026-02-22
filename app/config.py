from functools import lru_cache
from typing import List, Optional

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Core app
    app_name: str = "Research GenAI Chatbot Backend"
    app_env: str = "development"

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "chatbot_research"

    # CORS / frontend
    allowed_origins: List[str] = ["*"]

    # Qualtrics / Prolific redirects
    qualtrics_post_base_url: Optional[str] = None

    # LLM / OpenAI
    openai_api_key: str = "changeme"
    openai_base_url: str = "https://chat.binghamton.edu/api"
    openai_model: str = "llama3.2:latest"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1024

    # Memory: turns to include in the LLM payload
    memory_window: int = 20


@lru_cache()
def get_settings() -> Settings:
    return Settings()