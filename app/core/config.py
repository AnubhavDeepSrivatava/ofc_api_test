from typing import Union

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # APP
    # =========================
    PROJECT_NAME: str = "Microservice Template"
    API_V1_STR: str = "/api/v1"

    # =========================
    # DATABASE
    # =========================
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # This can be provided directly OR auto-built
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str] | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v, info) -> str:
        """
        If SQLALCHEMY_DATABASE_URI is provided in env → use it.
        Else → build it from individual POSTGRES_* variables.
        """
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=info.data.get("POSTGRES_DB"),
        )

    # =========================
    # REDIS (OPTIONAL)
    # =========================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env.example",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
