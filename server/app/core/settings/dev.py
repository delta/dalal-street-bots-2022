import logging

from pydantic import AnyHttpUrl, Field

from .app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True
    reload: bool = True
    title: str = "Dalal Street Bots - Dev"

    logging_level: int = logging.DEBUG

    grpc_server_uri: AnyHttpUrl = Field(...)
