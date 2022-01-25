"""Contains all the schema for bots db layer,
_"""

from datetime import datetime
from typing import Any, Dict, Literal, Union

from pydantic import BaseModel, Field, root_validator

from .timestamp import TimestampInDBPlugin


class BotBase(BaseModel):
    name: str
    bot_type: int


class BotInDB(BotBase, TimestampInDBPlugin):
    id: int

    class Config:
        orm_mode = True


class BotInDBInflated(BotInDB):
    """Bot db with bot_type data inflated"""

    # bot_type_id: int
    bot_type_name: str


class CreateBot(BotBase):
    pass


class QueryBot(BaseModel):
    name: str = Field("")
    bot_type: Union[str, int] = Field(0)

    _query_on = ""

    def get_query_on(cls) -> Literal["name", "bot_type"]:
        return cls._query_on

    @root_validator
    def check_valid_queried(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        "Checks if either of name or bot_type is given"
        is_valid_name = cls.name != ""
        is_valid_bot_type = False
        if type(cls.bot_type is str):
            if cls.bot_type == "":
                is_valid_bot_type = False
            else:
                is_valid_bot_type = True
        else:
            if cls.bot_type == 0:
                is_valid_bot_type = False
            else:
                is_valid_bot_type = True

        if not is_valid_name and not is_valid_bot_type:
            helpful_error_message = (
                f"query of `name='{cls.name}'` and `bot_type='{cls.bot_type}'` "
                + "is not valid. Provide one value for 'bot_type' or 'name'"
            )
            raise ValueError(helpful_error_message)
        if is_valid_bot_type and is_valid_name:
            # Both the values cannot be queried, only one can be queried at a time
            # so return a error
            helpful_error_message = (
                f"query of `name='{cls.name}'` and `bot_type='{cls.bot_type}'` "
                + "is not valid. You can only query with either one value of"
                " 'bot_type' or 'name'. You cannot provide both values."
            )
            raise (helpful_error_message)
        if is_valid_bot_type:
            cls._query_on = "bot_type"
        else:
            cls._query_on = "name"
        return values


def create_BotInDB_from_tuple(data: tuple) -> BotInDB:
    """Converts db row returned as tuple to pydantic model"""

    """Row Structure
        (id, name, bot_type, created_at, updated_at)
        ( 0,    1,        2,          3,          4)"""

    # TODO: Handle case when validation fails

    return BotInDB(
        id=data[0],
        name=data[1],
        bot_type=data[2],
        created_at=datetime(data[3]),
        updated_at=datetime(data[4]),
    )


def create_botInDBInflated_from_tuple(data: tuple) -> BotInDBInflated:
    """Converts db row returned as tuple to a pydantic model"""

    # BUG: We dont know what the columns will be, right now we are
    # hard-coding the order given in crud/bots/get_all_bots query
    # and this function will break (return unexpected result / fail validation)
    # when we change the column order,
    # POSSIBLE SOLUTION: cur.description() might provide some info
    # on how to solve this issue, need to check it later
    # (but the docs are non-existant, need to check source code )

    """Row Structure
        (id, name, bot_type, created_at, updated_at, bot_type_id, bot_type_name)
        ( 0,    1,        2,          3,          3,           4,             5)
        ### DIFFERENT FOR DIFFERENT QUERIES
    """

    return BotInDBInflated(
        id=data[0],
        name=data[1],
        bot_type=data[2],
        created_at=datetime(data[3]),
        updated_at=datetime(data[4]),
        bot_type_name=data[5],
    )
