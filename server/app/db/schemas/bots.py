"""Contains all the schema for bots db layer,
_"""

from typing import Any, Dict, Tuple, Union

from pydantic import BaseModel, Field, root_validator

from .timestamp import TimestampInDBPlugin


class BotBase(BaseModel):
    name: str
    bot_type: int
    server_bot_id: int


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
    server_bot_id: int = Field(0)

    _query_on = ""

    def get_query_on(cls) -> str:
        return cls._query_on

    @root_validator
    def check_valid_queried(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        "Checks if either of name or bot_type or server_bot_id is given"
        name = values.get("name", "")
        bot_type = values.get("bot_type", 0)
        server_bot_id = values.get("server_bot_id", 0)

        # checks to see if the values are valid
        is_valid_name = name != ""
        is_valid_server_bot_id = server_bot_id != 0
        # a more comprehensive check is needed for bot_type
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

        if not is_valid_name and not is_valid_bot_type and not is_valid_server_bot_id:
            helpful_multiple_query_error_message = (
                f"query of `name='{name}'`, `bot_type='{bot_type}'`"
                f"`server_bot_id={server_bot_id}` is not valid. Provide one"
                " value for 'bot_type' or 'name' or 'server_bot_id'"
            )
            raise ValueError(helpful_multiple_query_error_message)

        helpful_multiple_query_error_message = (
            f"query of `name='{name}'`, `bot_type='{bot_type}'`"
            f"`server_bot_id={server_bot_id}` is not valid. You can"
            "you can query on one of 'bot_type' or"
            " 'name' or 'server_bot_id'"
        )
        values["_query_on"] = ""
        if is_valid_bot_type:
            values["_query_on"] = "bot_type"
        if is_valid_name:
            # query_on shd not be truthy as we can only query on
            # 1 parameter
            if values["_query_on"]:
                raise ValueError(helpful_multiple_query_error_message)
            values["_query_on"] = "name"
        if is_valid_server_bot_id:
            if values["_query_on"]:
                raise ValueError(helpful_multiple_query_error_message)
            values["_query_on"] = "server_bot_id"

        # typecasting bot_type
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
        (id, name, bot_type, created_at, updated_at, server_bot_id)
        ( 0,    1,        2,          3,          4,             5)"""

    # TODO: Handle case when validation fails

    return BotInDB(
        id=data[0],
        name=data[1],
        bot_type=data[2],
        created_at=data[3],
        updated_at=data[4],
        server_bot_id=data[5],
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
    (id, name, bot_type, created_at, updated_at, server_bot_id, bot_type_id, bot_type_name) # noqa: E501
    ( 0,    1,        2,          3,          4,             5,           6,             7) # noqa: E501
        ### DIFFERENT FOR DIFFERENT QUERIES
    """

    return BotInDBInflated(
        id=data[0],
        name=data[1],
        bot_type=data[2],
        created_at=data[3],
        updated_at=data[4],
        server_bot_id=data[5],
        bot_type_name=data[7],
    )
