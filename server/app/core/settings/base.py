from dataclasses import Field
from pydantic import BaseSettings, Field, AnyHttpUrl, validator
from enum import Enum


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    """BaseSettings for the App"""

    app_env: AppEnvTypes = AppEnvTypes.prod

    @validator("app_env", pre=True)
    def check_if_valid_value(cls, v):
        if not v in AppEnvTypes._value2member_map_:
            # setting it to prod so that forgetting to set APP_ENV
            # doesn't cause any vulnerabilities
            print('Not a valid app_env provided, setting it to "prod" by default')
            return AppEnvTypes.prod
        return v

    class Config:
        env_file = ".env"
