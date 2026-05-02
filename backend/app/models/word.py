"""Word model — stores the valid Wordle word list, seeded from words.txt."""

from sqlmodel import Field, SQLModel


class Word(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    # Unique 5-letter word — indexed for fast lookup during guess validation
    word: str = Field(index=True, unique=True, max_length=5)
