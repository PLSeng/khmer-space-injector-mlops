from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_ENV_PATH = (_PROJECT_ROOT / ".env").resolve()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "khmer-space-injector-api"
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    CORS_ORIGINS: str = "http://localhost:5173"
    DATABASE_URL: str

    ARTIFACT_DIR: str = "artifacts"
    MAX_LEN: int = 128
    MAX_TEXT_CHARS: int = 200_000
    DEVICE: str = "cpu"

    ENABLE_DB_LOGGING: bool = True  
    ENABLE_HEALTH_DB_CHECK: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000


    @property
    def cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

    @property
    def artifact_path(self) -> Path:
        api_root = Path(__file__).resolve().parents[2]
        return (api_root / self.ARTIFACT_DIR).resolve()

settings = Settings()
