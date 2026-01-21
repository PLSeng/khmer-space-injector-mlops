from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",      # will be provided by docker compose env_file too
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "khmer-space-injector-api"
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    CORS_ORIGINS: str = "http://localhost:5173"

    DATABASE_URL: str | None = None

    ARTIFACT_DIR: str = "artifacts"
    MAX_LEN: int = 128
    MAX_TEXT_CHARS: int = 200_000
    DEVICE: str = "cpu"

    ENABLE_DB_LOGGING: bool = Field(default=False)

    @property
    def cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

    @property
    def api_root(self) -> Path:
        # config.py is apps/api/app/core/config.py
        # parents[2] => apps/api/app
        return Path(__file__).resolve().parents[2]

    @property
    def artifact_path(self) -> Path:
        # artifacts folder at apps/api/artifacts
        return (self.api_root.parent / self.ARTIFACT_DIR).resolve()

settings = Settings()