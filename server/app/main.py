from typing import Any

import uvicorn
from core.config import PORT
from fastapi import FastAPI
from grpc_manager.base import GrpcManager

app = FastAPI()


if __name__ == "__main__":
    grpc_manager = GrpcManager()
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

app = FastAPI(debug=True)


@app.get("/")
async def read_root() -> Any:
    # TODO: fix return type
    return {"Dalal": "ToTheMoon"}
