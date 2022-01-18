from typing import Any

import uvicorn
from core.config import get_app_settings
from fastapi import FastAPI
from grpc_manager.base import GrpcManager

app = FastAPI()


if __name__ == "__main__":
    grpc_manager = GrpcManager()
    uvicorn.run("main:app", host="0.0.0.0", port=get_app_settings().port)

app = FastAPI(**get_app_settings().fastapi_kwargs())


@app.get("/")
async def read_root() -> Any:
    # TODO: fix return type
    return {"Dalal": "ToTheMoon"}
