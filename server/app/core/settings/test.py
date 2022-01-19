import logging

from pydantic import AnyHttpUrl, Field

from .app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True
    reload: bool = True
    title: str = "Dalal Street Bots - Test"

    grpc_server_uri: AnyHttpUrl = Field(...)

    # db: DatabaseDsn = Field(DatabaseDsn(_env_file="test.env"))

    # Generally we would want to see debug level during test
    logging_level: int = logging.DEBUG

    class Config:
        # We have a separete env for testing
        # (which is yet to be implemented)
        env_file = "test.env"
