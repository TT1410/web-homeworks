from faker import Faker
from sqlalchemy.orm import Session

from database.models import Teacher
from .constants import NUM_TEACHERS


def create_teachers(session: Session, fake: Faker) -> None:
    session.add_all([Teacher(
        fullname=fake.name()) for _ in range(NUM_TEACHERS)]
    )
