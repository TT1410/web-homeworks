from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select, update, func, and_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.shemas.contacts import ContactModel, ContactUpdateModel, ContactPartialUpdateModel


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.scalar(
        select(Contact)
        .filter(Contact.id == contact_id)
    )


async def get_contacts(skip: int, limit: int, first_name: str, last_name: str, email: str,
                       db: Session) -> list[Contact]:
    query = select(Contact)

    if first_name:
        query = query.filter(Contact.first_name == first_name)
    if last_name:
        query = query.filter(Contact.last_name == last_name)
    if email:
        query = query.filter(Contact.email == email)

    contacts = db.execute(
        query.offset(skip).limit(limit)
    ).scalars().all()

    return contacts  # noqa


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def update_contact(contact_id: int, body: ContactUpdateModel, db: Session) -> Optional[Contact]:
    contact = db.execute(
        update(Contact)
        .values(**body.dict())
        .filter(Contact.id == contact_id)
        .returning(Contact)
    ).scalar()

    if contact:
        db.commit()

    return contact


async def partial_update_contact(contact_id: int, body: ContactPartialUpdateModel, db: Session) -> Optional[Contact]:
    contact_body = {key: val for key, val in body.dict().items() if val is not None}

    contact = db.execute(
        update(Contact)
        .values(**contact_body)
        .filter(Contact.id == contact_id)
        .returning(Contact)
    ).scalar()

    db.commit()

    return contact


async def remove_contact(contact_id: int, db: Session) -> Optional[Contact]:
    contact = await get_contact(contact_id, db)

    if contact:
        db.delete(contact)
        db.commit()

    return contact


async def get_contacts_birthdays(from_date: date, to_date: date, db: Session) -> list[Contact]:
    contacts = db.execute(
        select(Contact).filter(
            and_(
                func.to_char(Contact.birth_date, 'MM-DD') >= from_date.strftime("%m-%d"),
                func.to_char(Contact.birth_date, 'MM-DD') <= to_date.strftime("%m-%d")
            )
        )
    ).scalars().all()

    return contacts  # noqa
