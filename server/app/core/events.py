from typing import Callable

from db.connection import closeMySqlConnection, createMySqlConnection
from fastapi import FastAPI


def createStartAppHandler(app: FastAPI) -> Callable:  # type: ignore
    async def startApp() -> None:
        app.state.pool = await createMySqlConnection()
        return

    return startApp


def createStopAppHandler(app: FastAPI) -> Callable:  # type: ignore
    async def closeApp() -> None:
        await closeMySqlConnection(app.state.pool)
        return

    return closeApp
