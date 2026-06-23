from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_text_model: str = "gemini-2.5-flash"
    gemini_vision_model: str = "gemini-2.5-flash"
    gemini_embedding_model: str = "gemini-embedding-001"
    disable_gemini: bool = False
    backend_host: str = "127.0.0.1"
    backend_port: int = 8899

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
