from enum import Enum

from pydantic import BaseSettings, Field, validator

from .database import DatabaseDsn


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    """BaseSettings for the App"""

    app_env: AppEnvTypes = AppEnvTypes.prod

    db: DatabaseDsn = Field(DatabaseDsn(_env_file=".env"))  # type: ignore

    @validator("app_env", pre=True)
    def check_if_valid_value(cls, v: AppEnvTypes) -> AppEnvTypes:
        if v not in AppEnvTypes._value2member_map_:
            # setting it to prod so that forgetting to set APP_ENV
            # doesn't cause any vulnerabilities
            print('Not a valid app_env provided, setting it to "prod" by default')
            return AppEnvTypes.prod
        return v

    class Config:
        env_file = ".env"
