from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from sqlmodel import Session, SQLModel, select  # noqa: E402

from app.db import engine  # noqa: E402
from app.models.word import Word  # noqa: E402


def seed():
    SQLModel.metadata.create_all(engine)

    words_file = Path(__file__).parent.parent.parent / "app" / "data" / "words.txt"
    words = [
        w.strip().lower() for w in words_file.read_text().splitlines() if w.strip()
    ]

    with Session(engine) as session:
        existing = set(session.exec(select(Word.word)).all())
        new_words = [Word(word=w) for w in words if w not in existing and len(w) == 5]
        session.add_all(new_words)
        session.commit()
        print(f"Seeded {len(new_words)} words")


if __name__ == "__main__":
    seed()
