from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db.session import engine
from app.config import settings

# routers
from app.routers.api.items_api import router as items_router
from app.routers.api.health import router as health_router
from app.routers.api.auth_api import router as auth_router
from app.routers.api.requests_api import router as requests_router



app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(requests_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# CORS (open during dev)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# simple timing header
import time
from fastapi import Request
@app.middleware("http")
async def timing(request: Request, call_next):
    t0 = time.perf_counter()
    resp = await call_next(request)
    resp.headers["X-Server-Timing"] = f"total;dur={(time.perf_counter()-t0)*1000:.2f}"
    return resp

# mount routers
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router,   prefix=settings.API_V1_PREFIX)
app.include_router(items_router,  prefix=settings.API_V1_PREFIX)

# root
@app.get("/")
def root():
    return {"name": settings.PROJECT_NAME, "docs": f"{settings.API_V1_PREFIX}/docs".replace('//','/')}
