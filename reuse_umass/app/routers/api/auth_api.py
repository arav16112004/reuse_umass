from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/whoami")
def whoami():
    return {"user": "dev"}
