import logging
import os
from logging import Logger
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings
from sqlalchemy import URL, make_url


class Settings(BaseSettings):
    root: Path = (Path(__file__) / "../..").resolve()

    database_connect_args: dict[str, Any] = {"check_same_thread": False}
    database_engine_settings: dict[str, Any] = {"pool_size": 10, "max_overflow": 20}
    database_session_settings: dict[str, Any] = {
        "autocommit": False,
        "autoflush": False,
    }

    log_level: int = logging.DEBUG

    def model_post_init(self, context: Any) -> None:
        logging.basicConfig(level=self.log_level)

    @staticmethod
    def get_postgres_url(env_db_name: str) -> str:
        return (
            f"{os.getenv('POSTGRES_DRIVERNAME')}://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{env_db_name}"
        )

    @computed_field
    @property
    def postgres_prod_url(self) -> URL:
        return make_url(self.get_postgres_url(os.environ["POSTGRES_PROD_DBNAME"]))


settings = Settings()

load_dotenv(settings.root / ".env")


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)
    return logger
