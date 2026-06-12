from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.db.bootstrap import create_tables, seed_defaults
from app.db.session import AsyncSessionLocal
from app.security.middleware import ProductionSecurityMiddleware

settings = get_settings()
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.auto_create_tables:
        await create_tables()
        async with AsyncSessionLocal() as session:
            await seed_defaults(session)
        logger.info("startup.seeded", app=settings.app_name)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware that validates ingress requests and sanitizes payloads
app.add_middleware(ProductionSecurityMiddleware)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "offline_mode": settings.offline_mode,
    }


@app.get("/")
async def root():
    return {"name": settings.app_name, "docs": "/docs", "api": settings.api_v1_prefix}

