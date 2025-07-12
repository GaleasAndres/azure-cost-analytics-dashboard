"""Application configuration module."""

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    azure_client_id: str
    azure_tenant_id: str
    azure_client_secret: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
