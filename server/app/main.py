from typing import Any

import uvicorn
from core.config import get_app_settings
from core.events import createStartAppHandler, createStopAppHandler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.routes.api import router as ApiRouter
from api.routes.auth import router as AuthRouter

app = FastAPI()

origins = [get_app_settings().frontend_origin]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=get_app_settings().port,
        reload=get_app_settings().reload,
    )

app = FastAPI(**get_app_settings().fastapi_kwargs())


app.add_event_handler("startup", createStartAppHandler(app))
app.add_event_handler("shutdown", createStopAppHandler(app))

app.include_router(ApiRouter, tags=["api"], prefix="/api")
app.include_router(AuthRouter, tags=["auth"], prefix="/auth")


@app.get("/")
async def read_root() -> Any:
    # TODO: fix return type
    return {"Dalal": "ToTheMoon"}
