"""Database layer for Logs Table"""

from typing import Any, List
from aiomysql.cursors import Cursor
import logging
from pypika import Table, MySQLQuery, Order, Criterion, Query

from .base import log_query
import db.schemas.log as log_schema

logs = Table("logs")


async def insert_log(
    con: Cursor, log: str, log_level: log_schema.LogLevel, bot_id: int
) -> Exception:
    """Inserts a log into the database with the given data"""

    data = log_schema.InsertLog(log=log, level=log_level, bot_id=bot_id)
    q = (
        MySQLQuery.into(logs)
        .columns("id", "log", "level", "bot_id")
        .insert(None, data.log, data.level.name, data.bot_id)
    )
    logging.debug(f"Creating a new log for: {data.dict()}")
    log_query(str(q))
    try:
        await con.execute(str(q))
        await con.connection.commit()
    except Exception as e:
        logging.error(
            f"Couldn't create log for data={data.dict()} with the query={q} due to {e}"
        )


async def get_log_tail(
    con: Cursor, limit: int = 20, bot_id: int = 0, level: log_schema.LogLevel = None
):
    """Queries the and returns an last n logs satisfying the given parameters. User can fetch
    the last n logs by providing one or many of the given parameters,
    1. bot_id
    2. level - Log level of the log (INFO, WARN, DEBUG, ERROR)
    3. no of logs - No of tail logs you want to return, (By default, we fetch the last 20 logs)

    Args:
        con (Cursor): Sql Connection cursor
        limit (int, optional): Number of logs you want to fetch. Defaults to 20.
        bot_id (int, optional): Gets the logs for the bot with the given id.
        When not provided, it returns the logs of all the bots. Defaults to 0.
        level (log_schema.LogLevel, optional): Any specific level of logs you want to get.
        When not provided,it fetches all the levels . Defaults to None.
    _"""

    # validating the request
    # TODO:: handle validation error
    data = log_schema.GetLogTailRequest(limit=limit, bot_id=bot_id, level=level)

    # building constrains for the query
    # if a condition is passed to this func as a parameter
    # we append it to criteria
    criteria: List[Any] = []
    if bot_id != 0:
        criteria.append(logs.bot_id == bot_id)
    if level != None:
        criteria.append(logs.level == level.value.name)

    # Creating the query,
    # criteria constraint -> orderby  createdAt -> Limiting the queries
    q = (
        MySQLQuery.from_("logs")
        .select("*")
        .where(Criterion.all(criteria))
        .orderby(logs.created_at, order=Order.desc)
        .limit(limit)
    )

    logging.info(f"quering the logs with the criteria, {data.dict()}")
    log_query(str(q))
    # executing the query
    try:
        await con.execute(str(q))

        rows = await con.fetchall()
        """Row Schema
        (id, log, bot_id, level, created_at, updated_at)"""

        # TODO: This might throw an error, need to handle it
        resp = [log_schema.create_LogInDB_from_tuple(row) for row in rows]
        logging.debug(f"Got the response:{[x.dict() for x in resp]} when fetching queries")
        logging.info("Sucessfully fetched log/tail")
        # TODO: we are only returning response now, we also need to return any errors
        return resp

    except Exception as e:
        logging.error(
            f"Couldn't query the data={data.dict()} with the query={q} due to `{e}`"
        )
