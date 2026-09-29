from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Database
    database_url: str
    test_database_url: str

    # Redis
    redis_url: str
    test_redis_url: str

    # Rate limiting
    max_requests: int = 10
    window_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

settings = Settings()
