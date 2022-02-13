import asyncio
from datetime import datetime
import logging
from time import sleep
from typing import Any
import concurrent.futures

import uvicorn
from core.config import get_app_settings
from core.events import createStartAppHandler, createStopAppHandler
from fastapi import FastAPI, Request
from grpc_manager.base import GrpcManager, call_login_as_coroutine

app = FastAPI()


if __name__ == "__main__":
    grpc_manager = GrpcManager()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=get_app_settings().port,
        reload=get_app_settings().reload,
    )

app = FastAPI(**get_app_settings().fastapi_kwargs())


app.add_event_handler("startup", createStartAppHandler(app))
app.add_event_handler("shutdown", createStopAppHandler(app))


async def some_async_function():
    for i in range(10):
        logging.debug(i)
        await asyncio.sleep(2)
    logging.info("Completed the async loop")


def some_sync_function():
    for i in range(10):
        print(i)
        sleep(2)
    logging.info("Completed the sync loop")


@app.get("/")
async def read_root(request: Request) -> Any:
    # TODO: fix return type
    # await asyncio.run(some_async_function())
    # await some_async_function()
    # grpc: GrpcManager = request.app.state.grpc
    logging.info(f"got a reqest @ {datetime.now()}")
    # await call_login_as_coroutine()
    return {"Dalal": "ToTheMoon"}


@app.get("/hello")
async def read_root(request: Request) -> Any:
    # TODO: fix return type
    # grpc: GrpcManager = request.app.state.grpc
    logging.info(f"got a reqest for /hello @ {datetime.now()}")
    await sleep(10)
    # await call_login_as_coroutine()
    return {"Dalal": "ToTheMoon2"}


@app.get("/world")
async def world_handler() -> Any:
    loop = asyncio.get_running_loop()

    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, some_sync_function)
        return {"dalal": "ToTheWorld"}
