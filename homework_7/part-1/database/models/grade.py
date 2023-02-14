from datetime import date

from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base
from .student import Student
from .subject import Subject


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, default=date.today)
    student_id = Column(Integer, ForeignKey(
        Student.id, ondelete="cascade", onupdate="cascade")
    )
    subject_id = Column(Integer, ForeignKey(
        Subject.id, ondelete="cascade", onupdate="cascade")
    )
