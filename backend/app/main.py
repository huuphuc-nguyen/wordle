from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402 Ruff complaing about import order
from sqlmodel import SQLModel  # noqa: E402

from app.db import engine  # noqa: E402
from app.models import game, word  # noqa: E402, F401
from app.routers.game import router as game_router  # noqa: E402
from app.routers.health import router as health_router  # noqa: E402


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(game_router)
