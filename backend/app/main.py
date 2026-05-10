"""App entry point — loads config, registers models, mounts routers."""

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# load_dotenv must run before any module that calls os.getenv() at import time
load_dotenv()

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from sqlmodel import Session, SQLModel, select  # noqa: E402

from app.db import engine  # noqa: E402
from app.models import (  # noqa: E402, F401 — imported so SQLModel registers the tables
    game,
    word,
)
from app.models.word import Word  # noqa: E402
from app.routers.game import router as game_router  # noqa: E402
from app.routers.health import router as health_router  # noqa: E402

logger = logging.getLogger(__name__)

_DB_MAX_RETRIES = 30
_DB_RETRY_DELAY = 2  # seconds


def _wait_for_db() -> None:
    """Block until the database accepts a connection, or raise after max retries."""
    for attempt in range(1, _DB_MAX_RETRIES + 1):
        try:
            with engine.connect():
                pass
            logger.info("Database is ready")
            return
        except Exception as exc:
            logger.warning("DB not ready (attempt %d/%d): %s", attempt, _DB_MAX_RETRIES, exc)
            if attempt == _DB_MAX_RETRIES:
                raise RuntimeError("Database did not become ready in time") from exc
            time.sleep(_DB_RETRY_DELAY)


def _seed_words() -> None:
    """Seed the Word table from words.txt; no-op if already seeded."""
    with Session(engine) as session:
        if session.exec(select(Word).limit(1)).first():
            logger.info("Words already seeded — skipping")
            return

    words_file = Path(__file__).parent / "data" / "words.txt"
    words = [w.strip().lower() for w in words_file.read_text().splitlines() if w.strip()]
    new_words = [Word(word=w) for w in words if len(w) == 5]

    with Session(engine) as session:
        session.add_all(new_words)
        session.commit()
    logger.info("Seeded %d words", len(new_words))


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Wait for DB, create tables, seed words, then serve."""
    _wait_for_db()
    SQLModel.metadata.create_all(engine)
    _seed_words()
    yield


app = FastAPI(lifespan=lifespan, root_path="/apiwordle")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",          # Vite dev server
        "https://felixnguyen.dev",
        "https://wordle.felixnguyen.dev",
    ],
    allow_credentials=True,   # required for cookies to be sent cross-origin
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(game_router)
