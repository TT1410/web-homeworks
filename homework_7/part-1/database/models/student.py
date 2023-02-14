from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey(
        "groups.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    group = relationship("Group", back_populates="students", passive_deletes=True)
    subjects = relationship("Subject", secondary="grades", back_populates="students", passive_deletes=True)
