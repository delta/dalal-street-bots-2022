"""Contains all the schemas for data validation of botType CRUD functions
_"""

from typing import Any, Tuple

from pydantic import BaseModel

from .timestamp import TimestampInDBPlugin


class BotTypeBase(BaseModel):
    name: str


class InsertBotType(BotTypeBase):
    pass


class BotTypeInDB(BotTypeBase, TimestampInDBPlugin):
    id: int

    class Config:
        orm_mode = True


def create_BotTypeInDB_from_tuple(data: Tuple[Any, ...]) -> BotTypeInDB:
    """Utility function which creates a ButTypeInDB model from the database row."""

    """Row Structure
        (id, name, created_at, updated_at)
        ( 0,     1,         2,          3)"""

    # TODO: Handle case when validation fails
    return BotTypeInDB(id=data[0], name=data[1], created_at=data[2], updated_at=data[3])
