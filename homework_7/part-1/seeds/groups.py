from faker import Faker
from sqlalchemy.orm import Session

from database.models import Group
from .constants import NUM_GROUPS


def create_groups(sesssion: Session, fake: Faker) -> None:
    sesssion.add_all([Group(
        name=f"team_{num}") for num in range(1, NUM_GROUPS + 1)]
    )
