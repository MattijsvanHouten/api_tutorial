import logging
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings
from sqlalchemy import URL, make_url

logging.basicConfig()


class Settings(BaseSettings):
    cwd: Path = Path(__file__)

    database_url: URL = make_url("sqlite:///data/data.db")
    database_connect_args: dict[str, Any] = {"check_same_thread": False}
    database_engine_settings: dict[str, Any] = {"pool_size": 10, "max_overflow": 20}
    database_session_settings: dict[str, Any] = {
        "autocommit": False,
        "autoflush": False,
    }

    log_level: int = logging.DEBUG


settings = Settings()
