"""Database layer for bots"""

import logging
from typing import Any, List, Tuple, Union

import db.schemas.bots as bots_schema
from aiomysql.cursors import Cursor
from pydantic import ValidationError
from pypika import Criterion, MySQLQuery, Table

from .base import log_query, log_query_with_arguments
from .bot_types import get_bot_type_with_given_name

bots = Table("bots")


async def create_bot(
    con: Cursor, name: str, bot_type: Union[str, int], server_bot_id: int
) -> Tuple[bool, Union[Exception, None]]:
    """Creates a bot with the given name and bot_type.
    given bot_type can be either a str(bot_type.name) or int(bot_type.id)

    Returns True if the bot is successfully created, else (False, error)
    _"""

    bot_type_id: int = 0

    # validating bot data
    if type(bot_type) is int:
        # BUG: if the bot_type id is wrong, validation
        bot_type_id = bot_type
    else:
        # the bot_type name is given. get its id from bot_types
        # and update bot_id
        logging.debug("name of bot_type was given, fetching bot_type id from db")
        (bot_type_data, err) = await get_bot_type_with_given_name(con, str(bot_type))
        if err:
            # Some error occurred, return the error to the user
            return False, err
        logging.debug(
            f"Successfully found bot_type data={bot_type_data.dict()}"  # type: ignore
            f" when fetching bot_type with name={bot_type}"
        )
        bot_type_id = bot_type_data.id  # type: ignore

    try:
        data = bots_schema.CreateBot(
            name=name, bot_type=bot_type_id, server_bot_id=server_bot_id
        )
    except ValidationError as e:
        # error code = 1452, is thrown if the bot_type doesn't exist
        logging.error(f"Create bot validation failed due to {e.errors()}")
        return False, e

    logging.info(f"Trying to create a bot with data={data.dict()}")

    # Creating query
    q = (
        MySQLQuery.into(bots)
        .columns("name", "bot_type", "server_bot_id")
        .insert(data.name, data.bot_type, data.server_bot_id)
    )

    log_query(q)

    try:
        # executing query
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully created a bot with data={data.dict()}")
        return True, None
    except Exception as e:
        logging.error(
            f"Couldn't create bot with data={data.dict()}"
            f"with query=`{q}` due to `{e}`",
            stack_info=True,
        )
        return False, e


async def get_all_bots(
    con: Cursor, inflate_bot_type: bool = True
) -> Tuple[
    Union[List[bots_schema.BotInDB], List[bots_schema.BotInDBInflated]],
    Union[Exception, None],
]:
    """Finds and returns all the bots, optionally can pass on 'bot_type' to specify
    if you want to find the corresponding bot_type details and return it.

    Args:
        con (Cursor): AioMySql Connection
        inflate_bot_type (bool, optional): specify whether
        if you want to find the name of the corresponding bot_type
        row and return during response. Defaults to True.

    Returns:
        Tuple[List[bots_schema.BotInDB], Union[Exception, None]]: List of all the bots,
        Exception if any
    _"""

    logging.info(f"Finding all bots with {inflate_bot_type=}")

    q = (
        MySQLQuery.from_(bots).select("*")
        if inflate_bot_type is False
        else (
            "SELECT bots.*, \
        bot_types.id as bot_type_id,\
        bot_types.name as bot_type_name \
        from bots INNER JOIN bot_types ON bots.bot_type=bot_types.id"
        )
    )

    log_query(str(q))

    try:
        await con.execute(str(q))
        rows = await con.fetchall()
        """con.description -> example_response
        (
        ('id', 3, None, 11, 11, 0, False),
        ('name', 253, None, 1020, 1020, 0, False),
        ('bot_type', 3, None, 11, 11, 0, False),
        ('created_at', 7, None, 19, 19, 0, False),
        ('updated_at', 7, None, 19, 19, 0, False),
        ('server_bot_id', 3, None, 11, 11, 0, False),
        ('bot_type_id', 3, None, 11, 11, 0, False),
        ('bot_type_name', 253, None, 1020, 1020, 0, False))"""

        resp = (
            [bots_schema.create_botInDBInflated_from_tuple(row) for row in rows]
            if inflate_bot_type is True
            else [bots_schema.create_BotInDB_from_tuple(row) for row in rows]
        )
        logging.debug(
            f"got the resp:{[r.dict() for r in resp]} when querying for all the bots"
        )
        logging.info("successfully fetched all bots")
        return resp, None
    except Exception as e:
        logging.error(
            f"Couldn't query all bots with {inflate_bot_type=} with query={q}"
            f" due to {e}",
            exc_info=True,
        )
        return [], e


async def query_bots_with_details(
    con: Cursor,
    name: str = "",
    bot_type: Union[str, int] = 0,
    server_bot_id: int = 0,
    inflate_bot_type: bool = True,
) -> Tuple[
    Union[List[bots_schema.BotInDB], List[bots_schema.BotInDBInflated]],
    Union[Exception, None],
]:
    """Fetches all the bots with the queried details.
    name - returns Bots[] with the given name (List of len 1)
    bot_type - returns Bots[] of the given bot_type.
    bot_type can be int(bot_type.id) or str(bot_type.name) when bot_type.name
    is provided we fetch the bot_type with the given name and query the
    details

    additionally inflate_bot_type parameter can be passed so that bot_type details
    are fetched and returned to the user, this defaults to True (bot_type data is
    always inflated)"""

    if inflate_bot_type is True:
        return await _get_bots_with_details_inflated(con, name, bot_type, server_bot_id)
    else:
        return await _get_bots_with_details_uninflated(
            con, name, bot_type, server_bot_id
        )


async def _get_bots_with_details_inflated(
    con: Cursor, name: str = "", bot_type: Union[str, int] = 0, server_bot_id: int = 0
) -> Tuple[List[bots_schema.BotInDBInflated], Union[Exception, None]]:
    """Function to query inflated details"""

    logging.info(f"Quering bots with {name=}, {bot_type=}, {server_bot_id=} inflated")

    # validating data
    try:
        data = bots_schema.QueryBot(
            name=name, bot_type=bot_type, server_bot_id=server_bot_id
        )
    except ValidationError as e:
        # validation failed, return errors
        logging.error(
            f"Couldn't to query bots with {name=},{bot_type=} and {server_bot_id=}"
            f" as validation failed with the error(s): {e.errors()}",
            stack_info=True,
        )
        return [], e

    bot_id = 0
    if type(data.bot_type) is str and data.bot_type != "":
        # name of the bot_type is given, query for the bot_type_id and
        # use the to query the bot data
        logging.debug(
            f"bot_type.name=`{data.bot_type}` was given."
            "Trying to fetch its id from bot_type table"
        )
        bot_type_data, err = await get_bot_type_with_given_name(con, data.bot_type)
        if err:
            return [], err
        bot_id = bot_type_data.id  # type: ignore
    else:
        bot_id = data.bot_type

    # create the query
    # "AS" doesn't have proper support in pypika,
    # so we have to write our own query
    q = "SELECT bots.*, \
        bot_types.id as bot_type_id,\
        bot_types.name as bot_type_name \
        from bots INNER JOIN bot_types ON bots.bot_type=bot_types.id\
        WHERE "

    if data.get_query_on() == "name":
        q += "bots.name=%s"
        log_query_with_arguments(q, [data.name])
    elif data.get_query_on() == "server_bot_id":
        q += "bots.name=%s"
        log_query_with_arguments(q, [data.server_bot_id])
    else:
        q += "bots.bot_type=%s"
        log_query_with_arguments(q, [bot_id])

    try:
        if data.get_query_on() == "name":
            await con.execute(q, [data.name])
        else:
            await con.execute(q, [bot_id])
        rows = await con.fetchall()
        resp = [bots_schema.create_botInDBInflated_from_tuple(row) for row in rows]
        logging.debug(
            f"Got the response {[r.dict() for r in resp]} while querying for"
            f"bots with details {data.dict()}"
        )
        logging.info(f"Successfully found bots with data={data.dict()} inflated")
        return resp, None
    except Exception as e:
        logging.error(
            f"Couldn't query bots (inflated) with {data.dict()} with query={q}",
            f" and args={[data.name, bot_id, data.server_bot_id]} due to {e}",
            stack_info=True,
        )
        return [], None


async def _get_bots_with_details_uninflated(
    con: Cursor, name: str = "", bot_type: Union[str, int] = 0, server_bot_id: int = 0
) -> Tuple[List[bots_schema.BotInDB], Union[Exception, None]]:
    """Function to query uninflated details"""

    logging.info(
        f"Quering bots with {name=}, {bot_type=} and {server_bot_id=} uninflated"
    )

    # validating data
    try:
        data = bots_schema.QueryBot(
            name=name, bot_type=bot_type, server_bot_id=server_bot_id
        )
    except ValidationError as e:
        # validation failed, return errors
        logging.error(
            f"Couldn't to query bots with {name=}, {bot_type=} and {server_bot_id=}",
            f" as validation failed with the error(s): {e.errors()}",
            stack_info=True,
        )
        return [], e

    bot_id = 0
    if type(data.bot_type) is str:
        # name of the bot_type is given, query for the bot_type_id and
        # use the to query the bot data
        logging.debug(
            f"bot_type.name=`{data.bot_type}` was given."
            "Trying to fetch its id from bot_type table"
        )
        bot_type_data, err = await get_bot_type_with_given_name(con, data.bot_type)
        if err:
            # BUG: (minor, consitency)
            # We get a Record Not Found error if the bot_type == string
            # as we are checking for bot_type above
            # but if bot_type==int. we get No Error and empty List
            return [], err
        bot_id = bot_type_data.id  # type: ignore
    else:
        bot_id = data.bot_type

    criteria: List[Any] = []
    if data.get_query_on() == "name":
        criteria.append(bots.name == data.name)
    elif data.get_query_on() == "server_bot_id":
        criteria.append(bots.server_bot_id == data.server_bot_id)
    else:
        criteria.append(bots.bot_type == bot_id)

    # creating query
    # selecting * -> criteria contraint
    q = MySQLQuery.from_("bots").select("*").where(Criterion.all(criteria))

    log_query(str(q))
    # executing the query
    try:
        await con.execute(str(q))
        rows = await con.fetchall()
        resp = [bots_schema.create_BotInDB_from_tuple(row) for row in rows]
        logging.debug(
            f"Got the data {[r.dict() for r in resp]} when"
            f"fetching for data with {data.dict()}"
        )
        logging.info(f"Successfully found bots with data={data.dict()} uninflated")
        return resp, None
    except Exception as e:
        logging.error(
            "Couldn't query bots(uninflated) with"
            f"{data.dict()} with query={q} due to {e}",
            stack_info=True,
        )
        return [], None


async def update_bot_data_with_id(
    con: Cursor, id: int, name: str = "", bot_type: int = 0
) -> Tuple[bool, Union[Exception, None]]:
    """Update the data of the bot with the given id."""

    logging.info(
        "Trying to update the details of the bot with "
        f"{id=} to {name=} and {bot_type=}"
    )

    try:
        data = bots_schema.UpdateBot(name=name, bot_type=bot_type)
    except ValidationError as e:
        logging.error(
            f"Couldn't to update bots with {name=} and {bot_type=}",
            f" as validation failed with the error(s): {e.errors()}",
        )
        return False, e

    q = MySQLQuery.update(bots).where(bots.id == id)

    # manually checking if every query is dry, and
    # adding it to set
    if data.name != "":
        q = q.set(bots.name, data.name)
    if data.bot_type != 0:
        q = q.set(bots.bot_type, data.bot_type)

    log_query(str(q))

    try:
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully updated bot data to {data.dict()} with {id=}")
        return True, None
    except Exception as e:
        # TODO: Need to handle 1. invalid id, 2. duplicate name
        # Invalid id (no foregin key status code = 1452)
        logging.error(
            f"Unable to update bot data with {id=} to {data.dict()}"
            f" with query=`{q}` due to `{e}`"
        )
        return False, e


async def delete_bot_with_id(
    con: Cursor, id: int
) -> Tuple[bool, Union[Exception, None]]:
    """Deletes the bot with the given id"""

    logging.info(f"Trying to delete bot with {id=}")

    q = MySQLQuery.from_(bots).delete().where(bots.id == id)

    log_query(str(q))

    try:
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully deleted bot with {id=}")
        # BUG: no error is thrown when id doesn't exist
        return True, None
    except Exception as e:
        # TODO: Handle case when the bot with given id doesn't exist
        logging.error(
            f"Unable to delete bot with {id=} with query=`{q}` due to `{e}`",
            stack_info=True,
        )
        return False, e


async def delete_bot_with_given_name(
    con: Cursor, name: str
) -> Tuple[bool, Union[Exception, None]]:
    """deletes the bot with the given name"""

    logging.info(f"Trying to delete bot with {name=}")

    q = MySQLQuery.from_(bots).delete().where(bots.name == name)

    try:
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully deleted bot with {name=}")
        # BUG: no error is thrown when id doesn't exist
        return True, None
    except Exception as e:
        # TODO: Handle case when the bot with given name doesn't exist
        logging.error(
            f"Unable to delete bot with {name=} with query=`{q}` due to `{e}`",
            stack_info=True,
        )
        return False, e


async def delete_bot_with_given_server_bot_id(
    con: Cursor, server_bot_id: int
) -> Tuple[bool, Union[Exception, None]]:
    """deletes the bot with the given server_bot_id"""

    logging.info(f"Trying to delete bot with {server_bot_id=}")

    q = MySQLQuery.from_(bots).delete().where(bots.server_bot_id == server_bot_id)

    try:
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully deleted bot with {server_bot_id=}")
        # BUG: no error is thrown when id doesn't exist
        return True, None
    except Exception as e:
        # TODO: Handle case when the bot with given name doesn't exist
        logging.error(
            f"Unable to delete bot with {server_bot_id=} with query=`{q}` due to `{e}`",
            stack_info=True,
        )
        return False, e
