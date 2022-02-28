import logging

from .app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True
    reload: bool = True
    title: str = "Dalal Street Bots - Dev"

    logging_level: int = logging.DEBUG
