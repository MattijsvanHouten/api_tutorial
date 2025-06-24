import sqlalchemy as sa
from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy.orm import Session

from api.models import User as UserAPI
from api.models import UserCount as UserCountAPI
from api.services import fetch_user_count, fetch_users
from data.models import Base
from data.models import User as UserDB
from data.session import get_db, get_engine, get_session
from settings import get_logger, settings
from utils.helpers import get_or_create

logger = get_logger(__name__)

engine = get_engine(settings.database_url)
SessionLocal = get_session(engine)


# Create tables in the database if they don't exist
logger.info("Creating tables in the database if they don't exist...")
Base.metadata.create_all(bind=engine)


app = FastAPI(title="API tutorial", version="1.0")


@app.get("/users", response_model=list[UserAPI])
def get_all_users(db: Session = Depends(get_db)) -> list[UserAPI]:
    return fetch_users(db)


@app.get("/users/count", response_model=UserCountAPI)
def get_user_count(db: Session = Depends(get_db)) -> UserCountAPI:
    return fetch_user_count(db)


@app.get("/users/{id}", response_model=list[UserAPI])
def get_user(
    id: int = Path(..., title="User id", description="The id of an user"),
    db: Session = Depends(get_db),
) -> list[UserAPI]:
    result = fetch_users(db, id)
    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found!")
    return result


@app.post("/create", response_model=UserAPI)
def add_user(user: UserAPI, db: Session = Depends(get_db)) -> UserAPI:
    new_user = get_or_create(db, UserDB, name=user.name, email=user.email)
    return new_user


@app.delete("/users/{id}")
def delete_user(
    id: int = Path(..., title="User id", description="The id of an user"),
    db: Session = Depends(get_db),
) -> None:
    stmt = sa.select(UserDB).filter(UserDB.id == id)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
