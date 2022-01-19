from fastapi import FastAPI

from db.connection import createMySqlConnection, closeMySqlConnection


def createStartAppHandler(app: FastAPI):
    async def startApp():
        app.state.pool = await createMySqlConnection()
        return

    return startApp


def createStopAppHandler(app: FastAPI):
    async def closeApp():
        await closeMySqlConnection(app.state.pool)

    return closeApp
