from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "FeatureMaker"
    app_env: str = "dev"
    database_url: str = "postgresql+psycopg://featuremaker:featuremaker@localhost:65432/featuremaker"
    table_storage_dir: str = "data/table-assets"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
