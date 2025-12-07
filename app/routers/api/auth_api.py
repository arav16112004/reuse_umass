from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.sessions import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import hash_password, verify_password, create_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/whoami")
def whoami():
    return {"user": "dev"}

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserRead, status_code=201)
def signup(body: UserCreate, db: Session = Depends(get_session)):
    if db.exec(select(User).where(User.email == body.email)).first():
        raise HTTPException(400, "Email already registered")
    user = User(email=body.email, full_name=body.full_name, hashed_password=hash_password(body.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return Token(
        access_token=create_token(user.email, settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token=create_token(user.email, settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )

@router.get("/me", response_model=UserRead)
def me(user: User = Depends(lambda: None), db: Session = Depends(get_session)):


    from app.api.deps import get_current_user
    return get_current_user(db=db)  # type: ignore

@router.post("/seed-admin", response_model=UserRead)
def seed_admin(db: Session = Depends(get_session)):
    email = settings.ADMIN_EMAIL
    existing = db.exec(select(User).where(User.email == email)).first()
    if existing: return existing
    u = User(email=email, full_name="Admin", hashed_password=hash_password("admin"), is_superuser=True)
    db.add(u); db.commit(); db.refresh(u); return u
