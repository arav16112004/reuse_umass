from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

class ItemCreate(SQLModel):
    title: str
    description: str
    category: str
    condition: str
    location: str
    photo_url: Optional[str] = None
    owner_email: str

class ItemRead(SQLModel):
    id: int
    title: str
    description: str
    category: str
    condition: str
    location: str
    photo_url: Optional[str] = None
    owner_email: str
    created_at: datetime
    is_claimed: bool

class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    location: Optional[str] = None
    photo_url: Optional[str] = None
    is_claimed: Optional[bool] = None
