from pydantic import Field, HttpUrl

from .app import AppSettings


class ProdAppSettings(AppSettings):
    pass
