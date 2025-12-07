from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, String

class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(200), nullable=False))
    description: str = Field(sa_column=Column(String(2000), nullable=False))
    status: str = Field(default="open", sa_column=Column(String(32), index=True))  # open|in_progress|closed
    priority: int = Field(default=3, ge=1, le=5, index=True)  # 1 highest
    requester_email: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)
