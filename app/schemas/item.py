from typing import Optional
from sqlmodel import SQLModel

class ItemCreate(SQLModel):
    name: str
    price_cents: int

class ItemRead(SQLModel):
    id: int
    name: str
    price_cents: int
    is_active: bool

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    price_cents: Optional[int] = None
    is_active: Optional[bool] = None
