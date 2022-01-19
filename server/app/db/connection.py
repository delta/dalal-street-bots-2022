import asyncio
from aiomysql import Pool, create_pool

from core.config import get_app_settings


loop = asyncio.get_event_loop()


async def createMySqlConnection() -> Pool:
    """Creates a my sql connection pool along with the given settings
    and returns it"""

    async def create_db_with_given_loop(loop: asyncio.AbstractEventLoop):
        user = get_app_settings().db.user
        pwd = get_app_settings().db.pwd
        db_name = get_app_settings().db.name
        host = get_app_settings().db.host
        port = get_app_settings().db.port
        min_conn = get_app_settings().db.min_connection_count
        max_conn = get_app_settings().db.max_connection_count
        conn: Pool = await create_pool(
            host=host,
            port=port,
            user=user,
            password=pwd,
            db=db_name,
            minsize=min_conn,
            maxsize=max_conn,
            loop=loop,
        )

        return conn

    # loop.run_until_complete(create_db_with_given_loop(loop))
    return create_db_with_given_loop(loop)


async def closeMySqlConnection(pool: Pool) -> None:
    """Closes the mysql connection pool"""
    pool.close()
