from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.shemas.contacts import (
    ContactModel,
    ContactResponse,
    ContactUpdateModel,
    ContactPartialUpdateModel
)
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(current_user, body, db)
    return contact


@router.get("/birthdays", response_model=list[ContactResponse])
async def read_contact_birthdays(
                        from_date: Optional[date] = Query(
                            default=None,
                            description="Cannot be greater than {to_date} parameter. Example:",
                            example=date.today()),
                        to_date: Optional[date] = Query(
                            default=None,
                            description="Cannot be less than the {from_date} parameter.",
                            example=date.today() + timedelta(7)),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Get a list of contacts whose birthday falls within the selected time period. The period cannot exceed 7 days.

    If the **{from_date}** parameter is not specified, then a list of contacts whose birthday falls within the period
    **{to_date} - 7 days** will be returned.

    If the **{to_date}** parameter is not specified, then a list of contacts whose birthday falls within the period
    **{from_date} + 7 days** will be returned.

    If none of the parameters is specified, then a list of contacts whose birthday falls within the next 7 days
    from the current one will be returned.

    If the period is longer than 7 days, it will be truncated to 7 days from the **{from_date}** parameter.
    """
    if from_date and to_date:
        if from_date > to_date:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="The {from_date} parameter cannot be greater than the {to_date} parameter"
            )
        elif from_date + timedelta(days=7) < to_date:
            to_date = from_date + timedelta(days=7)
    else:
        if from_date is None and to_date:
            from_date = to_date + timedelta(7)
        elif to_date is None and from_date:
            to_date = from_date - timedelta(7)
        else:
            from_date = date.today()
            to_date = from_date + timedelta(7)

    return await repository_contacts.get_contacts_birthdays(current_user, from_date, to_date, db)


@router.get("/", response_model=list[ContactResponse], description="Get all contacts")
async def read_contacts(skip: int = 0, limit: int = Query(default=10, ge=1, le=100),
                        first_name: Optional[str] = Query(default=None, min_length=3, max_length=100),
                        last_name: Optional[str] = Query(default=None, min_length=3, max_length=100),
                        email: Optional[str] = Query(default=None),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contacts(current_user, skip, limit, first_name, last_name, email, db)

    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_note(body: ContactUpdateModel, contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse, description="At least one body field must be present!")
async def partial_contact_update(body: ContactPartialUpdateModel, contact_id: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.partial_update_contact(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
