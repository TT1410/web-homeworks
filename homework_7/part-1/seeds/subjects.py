from random import randint

from faker import Faker
from sqlalchemy.orm import Session

from database.models import Subject
from .constants import NUM_TEACHERS, NUM_DISCIPLINES


def create_subjects(sesssion: Session, fake: Faker):
    sesssion.add_all([Subject(
        name=fake.job(),
        teacher_id=randint(1, NUM_TEACHERS)) for _ in range(NUM_DISCIPLINES)]
    )
