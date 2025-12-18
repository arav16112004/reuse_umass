from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.sessions import get_session
from app.models.request import Request
from app.models.item import Item
from app.schemas.request import RequestCreate, RequestRead, RequestUpdate

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("", response_model=RequestRead, status_code=201)
def create_request(payload: RequestCreate, db: Session = Depends(get_session)):
    # verify item exists and is not claimed
    item = db.get(Item, payload.item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    if item.is_claimed:
        raise HTTPException(400, "Item is already claimed")
        
    obj = Request.model_validate(payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    
    # mock email notification
    print(f"--- MOCK EMAIL SENT ---")
    print(f"To: {item.owner_email}")
    print(f"Subject: New Request for {item.title}")
    print(f"Body: User {payload.requester_email} is interested in your item.")
    print(f"-----------------------")
    
    return obj

@router.get("", response_model=List[RequestRead])
def list_requests(
    db: Session = Depends(get_session),
    owner_email: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    stmt = select(Request)
    
    if owner_email:
        # join with item to filter by owner_email
        stmt = stmt.join(Item).where(Item.owner_email == owner_email)
        
    return db.exec(stmt.offset(offset).limit(limit)).all()

@router.get("/{request_id}", response_model=RequestRead)
def get_request(request_id: int, db: Session = Depends(get_session)):
    obj = db.get(Request, request_id)
    if not obj:
        raise HTTPException(404, "Request not found")
    return obj

@router.delete("/{request_id}", status_code=204)
def delete_request(request_id: int, db: Session = Depends(get_session)):
    obj = db.get(Request, request_id)
    if not obj:
        return
    db.delete(obj)
    db.commit()
