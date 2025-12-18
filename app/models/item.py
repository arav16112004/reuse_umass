from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    condition: str
    location: str
    photo_url: Optional[str] = None
    owner_email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_claimed: bool = False
