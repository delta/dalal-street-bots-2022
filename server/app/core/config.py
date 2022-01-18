from functools import lru_cache
from typing import Dict, Type

from .settings.app import AppSettings
from .settings.base import AppEnvTypes, BaseAppSettings
from .settings.dev import DevAppSettings
from .settings.prod import ProdAppSettings
from .settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
