from typing import Generator

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import sessionmaker

from data.models import Base
from settings import get_logger, settings

logger = get_logger(__name__)


def get_engine(url: URL) -> Engine:
    return create_engine(url, **settings.database_engine_settings)


def get_session(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, **settings.database_session_settings)


def get_db() -> Generator:
    logger.info("Connecting to database...")
    engine = get_engine(settings.postgres_prod_url)
    logger.debug("Engine: %s", engine)

    SessionLocal = get_session(engine)
    logger.debug("Session: %s", SessionLocal)

    db = SessionLocal()
    logger.debug("Db: %s", db)

    try:
        yield db
    finally:
        db.close()


def init_db():
    engine = get_engine(settings.postgres_prod_url)

    # Create tables in the database if they don't exist
    logger.info("Creating tables in the database if they don't exist...")
    Base.metadata.create_all(bind=engine)

    return get_session(engine)
