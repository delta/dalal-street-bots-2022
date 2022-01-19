from aiomysql import Pool, create_pool
from core.config import get_app_settings


async def createMySqlConnection() -> Pool:
    """Creates a my sql connection pool along with the given settings
    and returns it"""

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
    )

    return conn


async def closeMySqlConnection(pool: Pool) -> None:
    """Closes the mysql connection pool"""
    pool.close()
