from random import randint

from faker import Faker
from sqlalchemy.orm import Session

from database.models import Grade
from .constants import (
    NUM_STUDENTS,
    NUM_GRADES,
    NUM_DISCIPLINES
)


def create_grades(sesssion: Session, fake: Faker) -> None:
    sesssion.add_all([Grade(
        grade=randint(1, 12),
        date_of=fake.date_between(start_date='-1y'),
        student_id=randint(1, NUM_STUDENTS),
        subject_id=randint(1, NUM_DISCIPLINES)) for _ in range(NUM_STUDENTS * NUM_GRADES)]
    )
