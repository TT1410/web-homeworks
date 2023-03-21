from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas.users import UserModel


async def create_user(body: UserModel, db: Session) -> User:
    user = User(**body.dict())

    try:
        g = Gravatar(body.email)
        user.avatar = g.get_image()
    except Exception as e:
        print(e)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


async def get_user_by_email(email: str, db: Session) -> User:
    return db.execute(
        select(User)
        .filter(User.email == email)
    ).scalar()


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
