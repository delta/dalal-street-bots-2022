"""Database dependencies"""

from fastapi import Depends
from starlette.requests import Request
from aiomysql import Pool
from aiomysql.cursors import Cursor


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


def get_connection():
    """A FAST API Dependency which returns a cursor from the database
    connection pool. By using this function the user is guaranteed  to
    get a database cursor. Any route which requires some kind of database
    interation must use this dependency to access the database."""

    async def get_cursor_from_pool(pool: Pool = Depends(_get_db_pool)):
        conn = await pool.acquire()
        curr: Cursor = await conn.cursor()
        return curr

    return get_cursor_from_pool
