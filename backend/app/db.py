"""Database engine and session factory — shared across all services."""

import os

from sqlmodel import Session, create_engine

# Read from environment — loaded by main.py or seed_words.py before this module is imported
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)


def get_session():
    """FastAPI dependency — yields a database session and closes it after the request."""
    with Session(engine) as session:
        yield session
