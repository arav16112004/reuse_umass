from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel

class RequestCreate(SQLModel):
    title: str
    description: str
    requester_email: str
    priority: int = 3

class RequestRead(SQLModel):
    id: int
    title: str
    description: str
    status: str
    priority: int
    requester_email: str
    created_at: datetime
    updated_at: datetime

class RequestUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

# bulk helpers
class Ids(SQLModel):
    ids: List[int]

class BulkStatusUpdate(SQLModel):
    ids: List[int]
    status: str
