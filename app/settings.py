import os
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

# Détecter si on est dans un contexte de test (via pytest)
env_file = os.getenv("ENV_FILE")

if not env_file and any("pytest" in arg for arg in sys.argv):
    env_file = ".env.test"

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file or ".env",  # 👈 .env ou .env.test
        env_file_encoding="utf-8",
        extra="ignore"  # ignore les variables non définies
    )

settings = Settings()
