from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@localhost:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    # Указываем Pydantic точный абсолютный путь к файлу .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()