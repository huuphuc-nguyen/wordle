from pydantic import BaseModel, field_validator


class GuessRequest(BaseModel):
    word: str
