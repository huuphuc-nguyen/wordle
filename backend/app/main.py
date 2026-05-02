from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
from sqlmodel import SQLModel

from app.db import engine
from app.routers.game import router as game_router
from app.routers.health import router as health_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(game_router)
