from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.db.sessions import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.api.deps import get_current_active_superuser

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_session),
    _: User = Depends(get_current_active_superuser),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    stmt = select(User).offset(offset).limit(limit)
    return db.exec(stmt).all()

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_session), _: User = Depends(get_current_active_superuser)):
    u = db.get(User, user_id)
    if not u: raise HTTPException(404, "User not found")
    return u

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_session), _: User = Depends(get_current_active_superuser)):
    u = db.get(User, user_id)
    if not u: raise HTTPException(404, "User not found")
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items(): setattr(u, k, v)
    db.add(u); db.commit(); db.refresh(u); return u
