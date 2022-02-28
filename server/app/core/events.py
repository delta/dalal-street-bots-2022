import logging
from typing import Callable

from core.config import get_app_settings
from core.logger import setup_lg
from db.connection import closeMySqlConnection, createMySqlConnection
from fastapi import FastAPI
from grpc_manager.grpc_api import GrpcManager


def createStartAppHandler(app: FastAPI) -> Callable:  # type: ignore
    async def startApp() -> None:
        setup_lg()
        logging.info(f"Loading game with config={get_app_settings().dict()}")
        app.state.pool = await createMySqlConnection()
        app.state.grpc = GrpcManager()
        return

    return startApp


def createStopAppHandler(app: FastAPI) -> Callable:  # type: ignore
    async def closeApp() -> None:
        logging.info("Gracefully shutting down the app")
        await closeMySqlConnection(app.state.pool)
        app.state.grpc.close_connection()
        return

    return closeApp
