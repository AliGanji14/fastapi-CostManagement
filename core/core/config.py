from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "a_very_long_random_secret_key_at_least_32_bytes_long"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 900
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 604800
    COOKIE_SECURE: bool = False
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
