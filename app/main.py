from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from app.db.sessions import engine
from app.config import settings

# routers
from app.routers.api.items_api import router as items_router
from app.routers.api.health import router as health_router
from app.routers.api.auth_api import router as auth_router
from app.routers.api.requests_api import router as requests_router
from app.routers.frontend import router as frontend_router

app = FastAPI(title=settings.PROJECT_NAME)

# mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# cors (open during dev)
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
app.include_router(requests_router, prefix=settings.API_V1_PREFIX)

# frontend router (root)
app.include_router(frontend_router)
