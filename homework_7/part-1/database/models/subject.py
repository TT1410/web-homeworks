from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    teacher_id = Column(Integer, ForeignKey(
        "teachers.id", ondelete="set null", onupdate="cascade")
    )

    teacher = relationship("Teacher", back_populates="subjects", passive_deletes=True)
    students = relationship("Student", secondary="grades", back_populates="subjects", passive_deletes=True,)
