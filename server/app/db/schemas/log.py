from pydantic import BaseModel
from enum import IntEnum


class LogLevel(IntEnum):
    INFO = 1
    DEBUG = 2
    WARN = 3
    ERROR = 4


class LogBase(BaseModel):
    log: str
    level: LogLevel


class LogInDB(LogBase):
    id: int
    bot_id: str

    class Config:
        orm_mode = True


class InsertLog(LogBase):
    bot_id: str
