from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from api.models import User as UserAPI
from api.models import UserCount as UserCountAPI
from data.models import User as UserDB
from settings import get_logger

logger = get_logger(__name__)


def fetch_users(db: Session, user_id: Optional[int] = None) -> list[UserAPI]:
    stmt = sa.select(UserDB)
    if user_id:
        stmt = stmt.filter(UserDB.id == user_id)

    result = db.execute(stmt).scalars().all()
    if len(result) == 0:
        logger.warning("No users found!")

    return [UserAPI(name=u.name, email=u.email) for u in result]


def fetch_user_count(db: Session) -> UserCountAPI:
    stmt = sa.select(sa.func.count().label("count")).select_from(UserDB)

    result = db.execute(stmt).scalar_one_or_none()

    if not result:
        logger.warning("No users found!")

    return UserCountAPI(count=result)
