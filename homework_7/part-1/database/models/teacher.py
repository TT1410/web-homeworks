from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .subject import Subject


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)

    subjects = relationship(Subject, back_populates="teacher", passive_deletes=True)

    def __repr__(self):
        return ("Teacher({})".format(
            ', '.join([f"{k}={v!r}" for k, v in filter(lambda x: not x[0].startswith("_"), self.__dict__.items())]))
        )
