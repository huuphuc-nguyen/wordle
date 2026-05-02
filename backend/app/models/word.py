from sqlmodel import Field, SQLModel


class Word(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    word: str = Field(index=True, unique=True, max_length=5)
