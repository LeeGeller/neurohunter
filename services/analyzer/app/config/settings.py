"""Configuration settings."""

from pathlib import (
    Path,
)

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


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
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    email_host: str
    email_port: int
    email_user: str
    email_password: str
    email_from: str
    email_verification_url: str

    reset_password_token_secret: str
    verification_token_secret: str
    authentication_secret: str

settings = Settings()
