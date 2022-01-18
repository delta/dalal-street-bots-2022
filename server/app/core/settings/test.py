from pydantic import AnyHttpUrl, Field

from app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True
    reload: bool = True
    title: bool = "Dalal Street Bots - Test"

    grpc_server_uri: AnyHttpUrl = Field(...)

    # Need to set the Log level to Debug

    class Config:
        # We have a separete env for testing
        # (which is yet to be implemented)
        env_file = "test.env"
