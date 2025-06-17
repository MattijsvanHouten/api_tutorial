import logging
from typing import Any, Optional, TypeVar

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

from settings import settings

TBase = TypeVar("TBase", bound=DeclarativeBase)

logger = logging.getLogger(__file__)
logger.setLevel(settings.log_level)


def normalize_kwargs(model: TBase, kwargs: dict[str, Any]) -> dict[str, Any]:
    for column in model.__table__.columns:
        if column.name in kwargs and (
            kwargs[column.name] is None or kwargs[column.name] == ""
        ):
            kwargs[column.name] = None
        elif column.name in kwargs and isinstance(kwargs[column.name], str):
            kwargs[column.name] = kwargs[column.name].strip()
    return kwargs


def get_or_create(session: Session, model: TBase, **kwargs) -> Optional[TBase]:
    db_kwargs = normalize_kwargs(model, kwargs)

    stmt = sa.select(model).filter_by(**db_kwargs)

    try:
        instance = session.scalars(stmt).first()

        if instance:
            logger.debug("Existing record found in %s: %s", model.__name__, instance)
            return instance

        instance = model(**db_kwargs)
        session.add(instance)
        session.commit()
        logger.debug("Inserted new record into %s: %s", model.__name__, instance)

        return instance

    except IntegrityError:
        session.rollback()
        logger.debug(
            "IntegrityError in %s: %s. The record already exists. Prevent duplicate inserts.",
            model.__name__,
            db_kwargs,
        )
        return session.execute(stmt).scalars().first()

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(
            "Unexpected error in get_or_create for model %s", model.__name__, exc_info=e
        )
        return None
