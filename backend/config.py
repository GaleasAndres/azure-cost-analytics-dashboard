from pydantic import BaseSettings


class Settings(BaseSettings):
    azure_client_id: str = "YOUR_CLIENT_ID"
    azure_tenant_id: str = "YOUR_TENANT_ID"
    azure_client_secret: str = "YOUR_CLIENT_SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
