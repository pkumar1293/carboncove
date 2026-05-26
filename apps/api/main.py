"""CarbonCove FastAPI application."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from routers import health, estimate, calculate, reports, users, companies, installations
from db.database import engine
from models.db import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("AUTO_CREATE_TABLES", "false").lower() == "true":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="CarbonCove API",
    description="CBAM compliance calculation engine for Indian exporters",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

ALLOWED_ORIGINS = [
    "https://carboncove.in",
    "https://www.carboncove.in",
    "https://staging.carboncove.in",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"detail": str(exc)})


app.include_router(health.router)
app.include_router(estimate.router)
app.include_router(calculate.router)
app.include_router(reports.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(installations.router)
