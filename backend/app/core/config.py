from dataclasses import dataclass, field
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "Enterprise Document Processing OCR Platform"
    environment: str = field(default_factory=lambda: os.getenv("APP_ENV", "local"))
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "change-me-in-production"))
    access_token_minutes: int = field(default_factory=lambda: int(os.getenv("ACCESS_TOKEN_MINUTES", "120")))
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./storage/app.db"))
    upload_dir: Path = field(default_factory=lambda: Path(os.getenv("UPLOAD_DIR", "./storage/uploads")))
    allowed_origins: str = field(
        default_factory=lambda: os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5180,http://127.0.0.1:5180,http://localhost:8080",
        )
    )
    search_index_path: Path = field(default_factory=lambda: Path(os.getenv("SEARCH_INDEX_PATH", "./storage/search.json")))
    rate_limit_per_minute: int = field(default_factory=lambda: int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")))


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.search_index_path.parent.mkdir(parents=True, exist_ok=True)
    return settings
