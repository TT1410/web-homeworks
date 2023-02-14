from faker import Faker


from database.db import session
from .teachers import create_teachers
from .students import create_students
from .groups import create_groups
from .subjects import create_subjects
from .grades import create_grades


fake = Faker('uk_UA')


def create_fake_data() -> None:
    create_groups(session, fake)
    create_teachers(session, fake)
    create_students(session, fake)
    create_subjects(session, fake)
    create_grades(session, fake)

    session.commit()
