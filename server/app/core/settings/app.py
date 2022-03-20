import logging
from typing import Any, Dict

from .base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    reload: bool = False
    port: int = 8000

    logging_level: int = logging.INFO

    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Dalal Street Bots"

    grpc_server_port: int = 8000
    bot_secret: str = "hellobots"

    jwt_secret: str = "secure_secret"

    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "reload": self.reload,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
        }
