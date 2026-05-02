"""Seed script — populates the Word table from words.txt.

Run with: uv run python -m app.scripts.seed_words
"""

from pathlib import Path

from dotenv import load_dotenv

# load_dotenv before importing app modules so DATABASE_URL is available
load_dotenv()

from sqlmodel import Session, SQLModel, select  # noqa: E402

from app.db import engine  # noqa: E402
from app.models.word import Word  # noqa: E402


def seed():
    # Create the word table if it doesn't exist yet
    SQLModel.metadata.create_all(engine)

    # Resolve path relative to this file so the script works from any directory
    words_file = Path(__file__).parent.parent.parent / "app" / "data" / "words.txt"
    words = [
        w.strip().lower() for w in words_file.read_text().splitlines() if w.strip()
    ]

    with Session(engine) as session:
        # Skip words already in the table to make the script safe to run multiple times
        existing = set(session.exec(select(Word.word)).all())
        new_words = [Word(word=w) for w in words if w not in existing and len(w) == 5]
        session.add_all(new_words)
        session.commit()
        print(f"Seeded {len(new_words)} words")


if __name__ == "__main__":
    seed()
