"""App entry point — loads config, registers models, mounts routers."""

from contextlib import asynccontextmanager

from dotenv import load_dotenv

# load_dotenv must run before any module that calls os.getenv() at import time
load_dotenv()

from fastapi import FastAPI  # noqa: E402 Ruff complaing about import order
from sqlmodel import SQLModel  # noqa: E402

from app.db import engine  # noqa: E402
from app.models import (  # noqa: E402, F401 — imported so SQLModel registers the tables
    game,
    word,
)
from app.routers.game import router as game_router  # noqa: E402
from app.routers.health import router as health_router  # noqa: E402


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create all database tables on startup if they don't exist."""
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(game_router)
