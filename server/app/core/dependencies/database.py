"""Database dependencies"""

from aiomysql import Connection, Pool
from aiomysql.cursors import Cursor
from fastapi import Depends, Request


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


async def _get_db_connection(pool: Pool = Depends(_get_db_pool)) -> Connection:
    conn: Connection = await pool.acquire()
    try:
        yield conn
    finally:
        # BUG: Idk if we are supposed to close the connection after every request
        conn.close()


async def get_connection(conn=Depends(_get_db_connection)):
    """A FAST API Dependency which returns a cursor from the database
    connection pool. By using this function the user is guaranteed  to
    get a database cursor. Any route which requires some kind of database
    interation must use this dependency to access the database."""

    cursor: Cursor = await conn.cursor()
    try:
        yield (cursor)
    finally:
        await cursor.close()
