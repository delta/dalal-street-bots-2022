"""Contains all the schema for bots db layer,
_"""

from typing import Any, Dict, Tuple, Union

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

    def get_query_on(cls) -> str:
        return cls._query_on

    @root_validator
    def check_valid_queried(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        "Checks if either of name or bot_type is given"
        name = values.get("name", "")
        bot_type = values.get("bot_type", 0)
        is_valid_name = name != ""
        is_valid_bot_type = False
        if type(bot_type is str):
            if bot_type == "" or bot_type == "0":
                is_valid_bot_type = False
                values["bot_type"] = ""
            else:
                is_valid_bot_type = True
        else:
            if bot_type == 0:
                is_valid_bot_type = False
            else:
                is_valid_bot_type = True

        if not is_valid_name and not is_valid_bot_type:
            helpful_error_message = (
                f"query of `name='{name}'` and `bot_type='{bot_type}'` "
                "is not valid. Provide one value for 'bot_type' or 'name'"
            )
            raise ValueError(helpful_error_message)
        if is_valid_bot_type and is_valid_name:
            # Both the values cannot be queried, only one can be queried at a time
            # so return a error
            helpful_error_message = (
                f"query of `name='{name}'` and `bot_type='{bot_type}'` "
                "is not valid. You can only query with either one value of"
                " 'bot_type' or 'name'. You cannot provide both values."
            )
            raise ValueError(helpful_error_message)
        if is_valid_bot_type:
            values["_query_on"] = "bot_type"
        else:
            values["_query_on"] = "name"
        if str(bot_type).isnumeric():
            values["bot_type"] = int(bot_type)
        return values


class UpdateBot(BaseModel):
    name: str = Field("")
    bot_type: int = Field(0)

    @root_validator
    def check_valid_data(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Checks if at least one of name or bot_type is provided"""
        name = values.get("name", "")
        try:
            bot_type = int(values.get("bot_type", 0))
        except ValueError:
            raise ValueError(f"bot_type={values.get('bot_type')} is invalid")
        is_valid_name = name != ""
        is_valid_bot_type = bot_type != 0

        if not is_valid_bot_type and not is_valid_name:
            helpful_error_message = (
                f"query of `name='{name}'` and `bot_type='{bot_type}'` "
                "is not valid. Provide at least one value for"
                "'bot_type' or 'name'"
            )
            raise ValueError(helpful_error_message)

        return values


def create_BotInDB_from_tuple(data: Tuple[Any, ...]) -> BotInDB:
    """Converts db row returned as tuple to pydantic model"""

    """Row Structure
        (id, name, bot_type, created_at, updated_at)
        ( 0,    1,        2,          3,          4)"""

    # TODO: Handle case when validation fails

    return BotInDB(
        id=data[0],
        name=data[1],
        bot_type=data[2],
        created_at=(data[3]),
        updated_at=(data[4]),
    )


def create_botInDBInflated_from_tuple(data: Tuple[Any, ...]) -> BotInDBInflated:
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
        created_at=(data[3]),
        updated_at=(data[4]),
        bot_type_name=data[5],
    )
