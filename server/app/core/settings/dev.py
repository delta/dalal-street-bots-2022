from pydantic import AnyHttpUrl, Field

from .app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True
    reload: bool = True
    title: str = "Dalal Street Bots - Dev"

    grpc_server_uri: AnyHttpUrl = Field(...)  # type: ignore
