from __future__ import annotations
from typing import List, Optional, Tuple
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select
from sqlalchemy import func

from app.db.sessions import get_session
from app.models.request import Request
from app.schemas.request import (
    RequestCreate, RequestRead, RequestUpdate,
    Ids, BulkStatusUpdate
)

router = APIRouter(prefix="/requests", tags=["requests"])

def _apply_filters(
    stmt, q: Optional[str], status: Optional[str],
    email: Optional[str], created_from: Optional[datetime],
    created_to: Optional[datetime], min_priority: Optional[int],
    max_priority: Optional[int]
):
    if q:
        like = f"%{q}%"
        stmt = stmt.where((Request.title.ilike(like)) | (Request.description.ilike(like)))
    if status:
        stmt = stmt.where(Request.status == status)
    if email:
        stmt = stmt.where(Request.requester_email == email)
    if created_from:
        stmt = stmt.where(Request.created_at >= created_from)
    if created_to:
        stmt = stmt.where(Request.created_at < created_to)
    if min_priority is not None:
        stmt = stmt.where(Request.priority >= min_priority)
    if max_priority is not None:
        stmt = stmt.where(Request.priority <= max_priority)
    return stmt

def _with_count(db: Session, base_stmt) -> Tuple[int, any]:
    # total count (without limit/offset)
    total = db.exec(select(func.count()).select_from(base_stmt.subquery())).one()
    return total, base_stmt

@router.post("", response_model=RequestRead, status_code=201)
def create_request(payload: RequestCreate, db: Session = Depends(get_session)):
    obj = Request.model_validate(payload, update={})
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("", response_model=List[RequestRead])
def list_requests(
    response: Response,
    db: Session = Depends(get_session),
    q: Optional[str] = None,
    status: Optional[str] = None,
    email: Optional[str] = None,
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    min_priority: Optional[int] = Query(None, ge=1, le=5),
    max_priority: Optional[int] = Query(None, ge=1, le=5),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    stmt = select(Request)
    stmt = _apply_filters(stmt, q, status, email, created_from, created_to, min_priority, max_priority)

    # sorting
    sort_field = sort.lstrip("-")
    desc = sort.startswith("-")
    col = getattr(Request, sort_field, None)
    if col is None:
        raise HTTPException(400, f"Invalid sort field: {sort_field}")
    stmt = stmt.order_by(col.desc() if desc else col.asc())

    # total count header
    total, _ = _with_count(db, stmt)
    response.headers["X-Total-Count"] = str(total)

    rows = db.exec(stmt.offset(offset).limit(limit)).all()
    return rows

@router.get("/{request_id}", response_model=RequestRead)
def get_request(request_id: int, db: Session = Depends(get_session)):
    obj = db.get(Request, request_id)
    if not obj: raise HTTPException(404, "Request not found")
    return obj

@router.patch("/{request_id}", response_model=RequestRead)
def update_request(request_id: int, payload: RequestUpdate, db: Session = Depends(get_session)):
    obj = db.get(Request, request_id)
    if not obj: raise HTTPException(404, "Request not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{request_id}", status_code=204)
def delete_request(request_id: int, db: Session = Depends(get_session)):
    obj = db.get(Request, request_id)
    if not obj: return
    db.delete(obj); db.commit()

# ---- Bulk ops ----

@router.post("/bulk", response_model=List[RequestRead], status_code=201)
def bulk_create(payloads: List[RequestCreate], db: Session = Depends(get_session)):
    objs = [Request.model_validate(p, update={}) for p in payloads]
    db.add_all(objs); db.commit()
    for o in objs: db.refresh(o)
    return objs

@router.patch("/bulk/status", response_model=int)
def bulk_update_status(body: BulkStatusUpdate, db: Session = Depends(get_session)):
    changed = 0
    for rid in body.ids:
        obj = db.get(Request, rid)
        if obj:
            obj.status = body.status
            obj.updated_at = datetime.utcnow()
            db.add(obj)
            changed += 1
    db.commit()
    return changed

@router.delete("/bulk", status_code=204)
def bulk_delete(body: Ids, db: Session = Depends(get_session)):
    for rid in body.ids:
        obj = db.get(Request, rid)
        if obj:
            db.delete(obj)
    db.commit()
