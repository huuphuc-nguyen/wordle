"""APIResponse — standard envelope wrapping every response from the API."""

from typing import Any, Optional

from pydantic import BaseModel

from app.enums.api_status import APIStatus


class APIResponse(BaseModel):
    # Overall result of the request
    status: APIStatus

    # Human-readable message — mainly used for errors
    message: Optional[str] = None

    # The actual response payload — varies by endpoint
    data: Optional[Any] = None

    # HTTP-style status code included in the body for easy FE handling
    code: int
