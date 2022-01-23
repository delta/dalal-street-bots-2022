"""Database dependencies"""

from fastapi import Depends
from fastapi import Request
from aiomysql import Pool, Connection
from aiomysql.cursors import Cursor


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


async def _get_db_connection(pool: Pool = Depends(_get_db_pool)) -> Connection:
    conn: Connection = await pool.acquire()
    try:
        yield conn
    finally:
        print("Closing connection")
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
        print("Closing cursor")
        await cursor.close()
