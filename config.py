from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    DB_URL: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = BASE_DIR / '.env'


settings = Settings()
