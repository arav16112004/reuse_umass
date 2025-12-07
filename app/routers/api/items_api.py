from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.sessions import get_session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_session)):
    obj = Item.model_validate(payload, update={})
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("", response_model=List[ItemRead])
def list_items(
    db: Session = Depends(get_session),
    q: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    stmt = select(Item)
    if q:
        stmt = stmt.where(Item.name.ilike(f"%{q}%"))
    if is_active is not None:
        stmt = stmt.where(Item.is_active == is_active)
    return db.exec(stmt.offset(offset).limit(limit)).all()

@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_session)):
    obj = db.get(Item, item_id)
    if not obj:
        raise HTTPException(404, "Item not found")
    return obj

@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_session)):
    obj = db.get(Item, item_id)
    if not obj:
        raise HTTPException(404, "Item not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_session)):
    obj = db.get(Item, item_id)
    if not obj:
        return
    db.delete(obj)
    db.commit()
