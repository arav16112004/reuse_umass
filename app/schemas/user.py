from typing import Optional
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserRead(SQLModel):
    id: int
    email: str
    full_name: Optional[str] = None

class Token(SQLModel):
    access_token: str
    token_type: str
