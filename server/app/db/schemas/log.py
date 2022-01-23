"""Contains all the models for the database layer
Contains models for inserting, querying, log_in_db models
Any validation required for log's database layer must be done here,
so that only the actual query happens in crud/logs.py
_"""
from typing import Union
from pydantic import BaseModel
from enum import IntEnum

from datetime import datetime

from .timestamp import TimestampInDBPlugin


class LogLevel(IntEnum):
    INFO = 1
    DEBUG = 2
    WARN = 3
    ERROR = 4


class LogBase(BaseModel):
    log: str
    level: LogLevel


class LogInDB(LogBase, TimestampInDBPlugin):
    id: int
    bot_id: str

    class Config:
        orm_mode = True


class InsertLog(LogBase):
    bot_id: str


class GetLogTailRequest(BaseModel):
    level: Union[LogLevel, None]
    limit: int = 20
    bot_id: int = 0
