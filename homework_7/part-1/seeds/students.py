from random import randint

from faker import Faker
from sqlalchemy.orm import Session

from database.models import Student
from .constants import NUM_STUDENTS, NUM_GROUPS


def create_students(session: Session, fake: Faker) -> None:
    session.add_all([Student(
        fullname=fake.name(),
        group_id=randint(1, NUM_GROUPS)) for _ in range(NUM_STUDENTS)]
    )
