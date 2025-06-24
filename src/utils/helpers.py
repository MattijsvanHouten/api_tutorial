import logging
from typing import Any, Optional, TypeVar

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

from settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)

TBase = TypeVar("TBase", bound=DeclarativeBase)
TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


def normalize_kwargs(model: TBase, kwargs: dict[str, Any]) -> dict[str, Any]:
    for column in model.__table__.columns:
        col_name = column.name
        if col_name in kwargs:
            value = kwargs[col_name]
            if value in ("", None):
                kwargs[col_name] = None
            elif isinstance(value, str):
                kwargs[col_name] = value.strip()

    return kwargs


def get_or_create(session: Session, model: TBase, **kwargs) -> Optional[TBase]:
    db_kwargs = normalize_kwargs(model, kwargs)
    stmt = sa.select(model).filter_by(**db_kwargs)

    try:
        instance = session.scalars(stmt).first()
        if instance:
            logger.debug("Found existing %s: %s", model.__name__, instance)
            return instance

        instance = model(**db_kwargs)
        session.add(instance)
        session.commit()
        logger.debug("Created new %s: %s", model.__name__, instance)
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


def orm_to_pydantic(
    db: Session, obj: type[TBaseModel], query: sa.select
) -> list[TBaseModel]:
    result = db.execute(query).all()

    if not result:
        return []

    return [
        obj(**{k: v for k, v in zip(obj.model_fields.keys(), row)}) for row in result
    ]
