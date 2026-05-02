"""APIStatus — top-level status field used in every APIResponse envelope."""

from enum import Enum


class APIStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
