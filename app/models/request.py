from typing import Optional
from sqlmodel import SQLModel, Field

class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    requester_email: str
