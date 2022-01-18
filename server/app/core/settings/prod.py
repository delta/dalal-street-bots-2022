from pydantic import Field, HttpUrl

from .app import AppSettings


class ProdAppSettings(AppSettings):

    # In production, grpc url must bt a proper url with
    # a valid top-level domain
    grpc_server_uri: HttpUrl = Field(...)
