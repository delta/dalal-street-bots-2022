"""Database layer for Logs Table"""

from typing import Union, Tuple
from aiomysql.cursors import Cursor
import logging
from pypika import Table, MySQLQuery

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
        x = await con.fetchone()
        await con.connection.commit()
    except Exception as e:
        logging.error(
            f"Couldn't create log for data={data.dict()} with the query={q} due to {e}"
        )
