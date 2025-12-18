from typing import Optional
from sqlmodel import SQLModel

class RequestCreate(SQLModel):
    item_id: int
    requester_email: str

class RequestRead(SQLModel):
    id: int
    item_id: int
    requester_email: str

class RequestUpdate(SQLModel):
    requester_email: Optional[str] = None
