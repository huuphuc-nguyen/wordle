# app/enums/api_status.py

from enum import Enum


class APIStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
