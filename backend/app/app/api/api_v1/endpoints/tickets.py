from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.models.user import User as DBUser
from app.schemas.ticket import Ticket, TicketCreate, TicketUpdate

router = APIRouter()


@router.get("/", response_model=List[Ticket])
def read_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Retrieve Tickets.
    """
    if crud.user.is_superuser(current_user):
        tickets = crud.ticket.get_multi(db, skip=skip, limit=limit)
    else:
        tickets = crud.ticket.get_multi_by_owner(
            db_session=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return tickets


@router.post("/", response_model=Ticket)
def create_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_in: TicketCreate,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Create new ticket.
    """
    ticket = crud.ticket.create_with_owner(
        db_session=db, obj_in=ticket_in, owner_id=current_user.id
    )
    return ticket


@router.put("/{id}", response_model=Ticket)
def update_ticket(
    *,
    db: Session = Depends(get_db),
    id: int,
    ticket_in: TicketUpdate,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Update an Ticket.
    """
    ticket = crud.ticket.get(db_session=db, id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    if not crud.user.is_superuser(current_user) and (ticket.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ticket = crud.ticket.update(db_session=db, db_obj=ticket, obj_in=ticket_in)
    return ticket


@router.get("/{id}", response_model=Ticket)
def read_ticket(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get Ticket by ID.
    """
    ticket = crud.ticket.get(db_session=db, id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    if not crud.user.is_superuser(current_user) and (ticket.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return ticket


@router.delete("/{id}", response_model=Ticket)
def delete_ticket(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Delete an Ticket.
    """
    ticket = crud.ticket.get(db_session=db, id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="ticket not found")
    if not crud.user.is_superuser(current_user) and (ticket.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ticket = crud.ticket.remove(db_session=db, id=id)
    return ticket
