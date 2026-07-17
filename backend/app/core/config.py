from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = "Enterprise Document Processing OCR Platform"
    environment: str = os.getenv("APP_ENV", "local")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "120"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./storage/app.db")
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", "./storage/uploads"))
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    search_index_path: Path = Path(os.getenv("SEARCH_INDEX_PATH", "./storage/search.json"))


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.search_index_path.parent.mkdir(parents=True, exist_ok=True)
    return settings

