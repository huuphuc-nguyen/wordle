from typing import Any, Optional

from pydantic import BaseModel

from app.enums.api_status import APIStatus


class APIResponse(BaseModel):
    status: APIStatus
    message: Optional[str] = None
    data: Optional[Any] = None
    code: int
