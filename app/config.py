from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/license_manager"

    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_client_secret: str = ""

    brity_api_url: str = ""
    brity_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
