"""Contains all the schemas for the database layer
Contains models for inserting, querying, log_in_db models
Any validation required for log's database layer must be done here,
so that ONLY the actual query execution happens in crud/logs.py
_"""
from enum import IntEnum
from typing import Any, Tuple, Union

from pydantic import BaseModel

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


def create_LogInDB_from_tuple(data: Tuple[Any, ...]) -> LogInDB:
    """A Utility function which creates a LogInDB model from a database Row.
    When we get data from db, it is returned to us as a tuple and there isn't
    a proper way to parse it into a pydantic model,
    refer https://github.com/tiangolo/fastapi/issues/214

    So we have to write our own parser"""

    """Row Structure
        (id, log, bot_id, level, created_at, updated_at)
        (  0,  1,      2,     3,          4,          5)"""

    # TODO: Handle case when validation fails
    return LogInDB(
        id=data[0],
        log=data[1],
        bot_id=data[2],
        level=LogLevel[data[3]],
        created_at=(data[4]),
        updated_at=(data[5]),
    )
