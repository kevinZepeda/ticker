from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.models.user import User as DBUser
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Retrieve Tikets.
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db_session=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=Item)
def create_ticket(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Create new Ticket.
    """
    item = crud.item.create_with_owner(
        db_session=db, obj_in=item_in, owner_id=current_user.id
    )
    return item


@router.put("/{id}", response_model=Item)
def update_ticket(
    *,
    db: Session = Depends(get_db),
    id: int,
    item_in: ItemUpdate,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Update an Ticket.
    """
    item = crud.item.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.update(db_session=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=Item)
def read_ticket(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get Ticket by ID.
    """
    item = crud.item.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.delete("/{id}", response_model=Item)
def delete_ticket(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Delete an Ticket.
    """
    item = crud.item.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.remove(db_session=db, id=id)
    return item
