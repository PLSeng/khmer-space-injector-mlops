from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "khmer-space-injector-api"
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    CORS_ORIGINS: str = "http://localhost:5173"

    DATABASE_URL: str

    ARTIFACT_DIR: str = "artifacts"
    MAX_LEN: int = 128
    MAX_TEXT_CHARS: int = 200_000
    DEVICE: str = "cpu"

    @property
    def cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

    @property
    def artifact_path(self) -> Path:
        # apps/api/app/core/config.py -> apps/api/
        api_root = Path(__file__).resolve().parents[2]
        return (api_root / self.ARTIFACT_DIR).resolve()

settings = Settings()  # reads from env/.env
