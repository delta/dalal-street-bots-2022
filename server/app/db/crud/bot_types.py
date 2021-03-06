"""Database layer for 'bot_types' Table"""
import logging
from typing import List, Tuple, Union

import db.schemas.bot_types as bot_type_schema
import pymysql
from aiomysql.cursors import Cursor
from db.errors import RecordNotFound
from pydantic import ValidationError
from pypika import MySQLQuery, Table

from .base import log_query

bot_types = Table("bot_types")

# TODO: add type validation to request


async def insert_bot_type(
    con: Cursor, name: str
) -> Tuple[bool, Union[Exception, None]]:
    """Inserts a bot_type into the database with the given data"""

    logging.info(f"Trying to insert a new 'bot_type' with {name=}")

    # validating the data
    try:
        data = bot_type_schema.InsertBotType(name=name)
    except ValidationError as e:
        logging.error(f"InsertBotTypeValidation failed, error:{e.errors()}")
        return False, e

    # Generating mysql query
    q = MySQLQuery.into(bot_types).columns("name").insert(data.name)
    log_query(str(q))

    try:
        # executing query
        await con.execute(str(q))
        # commiting the query
        await con.connection.commit()
        logging.info("Successfully added the bot_type to database")
        return True, None
    except Exception as e:
        # TODO: return a special response for not_unique_error
        # not unique error has status_code=1062
        if type(e) == pymysql.err.IntegrityError:
            x = e.args[0] == 1062
            logging.debug(f"isDuplicateKey={x}")
        logging.error(
            f"Couldn't create new bot_type for data={data.dict()} with {q} due to {e}"
        )
        return False, e


async def get_all_bot_types(
    con: Cursor,
) -> Tuple[List[bot_type_schema.BotTypeInDB], Union[Exception, None]]:
    """Fetches all the bots from the database"""
    logging.info("Trying to fetch all bots")

    # creating query
    q = MySQLQuery.from_(bot_types).select("*")

    log_query(str(q))

    try:
        await con.execute(str(q))

        rows = await con.fetchall()
        # TODO: This might throw an error, need to handle it
        resp = [bot_type_schema.create_BotTypeInDB_from_tuple(row) for row in rows]
        logging.debug(
            f"Got the response:{[x.dict() for x in resp]} when fetching queries"
        )
        logging.info("Successfully fetched all the bot_types data")
        return resp, None

    except Exception as e:
        logging.error(f"Couldn't query all bot_types with the query={q} due to `{e}`")
        return [], e


async def check_if_bot_type_with_given_data_exists(
    con: Cursor, data: Union[int, str]
) -> bool:
    """Checks if a bot_type with the given name or id exists"""
    try:
        if type(data) == int or data.isnumeric():
            resp, err = await get_bot_type_with_given_id(con, data)
        else:
            resp, err = await get_bot_type_with_given_name(con, data)

        assert not err
        assert resp
        return True
    except AssertionError:
        return False


async def get_bot_type_with_given_name(
    con: Cursor, name: str
) -> Tuple[Union[bot_type_schema.BotTypeInDB, None], Union[Exception, None]]:
    """Fetch bot with given name"""

    logging.info(f"Trying the fetch bot_type with {name=}")

    # creating query
    q = MySQLQuery.from_(bot_types).select("*").where(bot_types.name == name)

    log_query(str(q))

    try:
        await con.execute(str(q))
        row = await con.fetchone()
        # response, need to check it
        if row is None:
            logging.error(f"bot_type with {name=} doesn't exist")
            return None, RecordNotFound
        resp = bot_type_schema.create_BotTypeInDB_from_tuple(row)
        logging.debug(f"for the data={resp.dict()} while fetching bot with {name=}")
        logging.info(f"Successfully fetched the bot with {name=}")
        return resp, None
    except Exception as e:
        logging.error(f"Unable to query with {name=} with query={q} due to `{e}`")
        return None, e


async def get_bot_type_with_given_id(
    con: Cursor, id: int
) -> Tuple[Union[bot_type_schema.BotTypeInDB, None], Union[Exception, None]]:
    """Fetches the bot with the given id"""
    logging.info(f"Trying the fetch bot_type with {id=}")

    # creating query
    q = MySQLQuery.from_(bot_types).select("*").where(bot_types.id == id)

    log_query(str(q))

    # executing the query
    try:
        await con.execute(str(q))
        row = await con.fetchone()
        # response is None if the record does not exist
        if row is None:
            logging.error(f"bot_type with {id=} doesn't exist")
            return None, RecordNotFound
        resp = bot_type_schema.create_BotTypeInDB_from_tuple(row)
        logging.debug(f"for the data={resp.dict()} while fetching bot with {id=}")
        logging.info(f"Successfully fetched the bot with the {id=}")
        return resp, None
    except Exception as e:
        logging.error(f"Unable to query with {id=} with query={q} due to `{e}`")
        return None, e


async def update_bot_type_name(
    con: Cursor, id: int, name: str
) -> Tuple[bool, Union[Exception, None]]:
    """Changes the name of the the bot with the given id"""

    logging.info(f"Trying to the name of the bot with {id=}, to {name}")

    # TODO: Add data validation
    # BUG: Need to check if the bot with the given id exists

    # creating query
    q = MySQLQuery.update(bot_types).set(bot_types.name, name).where(bot_types.id == id)

    log_query(str(q))

    try:
        await con.execute(str(q))
        await con.connection.commit()
        # ! Error is not thrown if a bot with the given id doesn't exist
        logging.info(f"Successfully updated bot_type name to `{name}` with {id=}")
        return True, None
    except Exception as e:
        # TODO: Need to handle 1. invalid id, 2. duplicate name
        logging.error(
            f"Unable to update bot_type with {id=} to {name=} with query=`{q}`"
            f"due to `{e}`"
        )
        return False, e


async def delete_bot_type_with_given_id(
    con: Cursor, id: int
) -> Tuple[bool, Union[Exception, None]]:
    """deletes the bots with the given id"""

    logging.info(f"Trying to delete bot with {id=}")

    q = MySQLQuery.from_(bot_types).delete().where(bot_types.id == id)

    log_query(str(q))

    try:
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully deleted bot_type with {id=}")
        return True, None
    except Exception as e:
        # TODO: Handle case when the bot with given id doesn't exist
        logging.error(
            f"Unable to delete bot_type with {id=} with query=`{q}` due to `{e}`"
        )
        return False, e


async def delete_bot_type_with_given_name(
    con: Cursor, name: str
) -> Tuple[bool, Union[Exception, None]]:
    """deletes the bots with the given name"""

    logging.info(f"Trying to delete bot with {name=}")

    q = MySQLQuery.from_(bot_types).delete().where(bot_types.name == name)

    try:
        await con.execute(str(q))
        await con.connection.commit()
        logging.info(f"Successfully deleted bot_type with {name=}")
        return True, None
    except Exception as e:
        # TODO: Handle case when the bot with given name doesn't exist
        logging.error(
            f"Unable to delete bot_type with {name=} with query=`{q}` due to `{e}`"
        )
        return False, e
