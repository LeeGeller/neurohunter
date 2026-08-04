"""Configuration settings."""

from pathlib import (
    Path,
)

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

PROJECT_ROOT = Path(__file__).resolve().parents[4]

print("PROJECT_ROOT:", PROJECT_ROOT)
print("ENV PATH:", PROJECT_ROOT / ".env")
print("ENV EXISTS:", (PROJECT_ROOT / ".env").exists())

class Settings(BaseSettings):
    """Application settings."""

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    mongo_uri: str
    mongo_db: str
    mongo_port: int

    ollama_host: str
    ollama_model: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
