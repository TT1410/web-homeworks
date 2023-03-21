from sqlalchemy import Column, Integer, Date, String, Boolean, func, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True)
    email = Column(String(250), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)


class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = (
        UniqueConstraint('email', 'user_id', name='unique_contact_user'),
    )

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=False, index=True)
    phone_number = Column(String(20), nullable=False)
    birth_date = Column(Date, nullable=False)
    additional_data = Column(String(500))
    user_id = Column(ForeignKey(User.id, ondelete="CASCADE"), nullable=False)

    user = relationship(User, backref="contacts")
