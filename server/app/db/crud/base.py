import logging
from typing import Any, List


def log_query(query: str) -> None:
    logging.debug(f"Executing query:'{query}'")
    return


def log_query_with_arguments(query: str, args: List[Any]) -> None:
    logging.debug(f"Executing query:`{query}` with {args=}")
    return
