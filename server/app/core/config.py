import os

from dotenv import dotenv_values

# TODO: add pydantic models to it


def convertToInt(key: str, default: int) -> int:
    data = config.get(key, str(default))
    if data is None:
        return default
    else:
        return int(data)


_dir_path = os.path.dirname(os.path.realpath(__file__))
_path = _dir_path + "/../../.env"
config = dotenv_values(_path)
# TODO: Clean this up
PORT = convertToInt("PORT", 8001)

# TODO: it would be nice if we add some check to see
# if the env contains "http" or "https", and throw an error
GRPC_SERVER_URI = config.get("GRPC_SERVER_URI", "localhost:8000")

DB_NAME = config.get("DB_NAME", "dalal_street_bots")
DB_PWD = config.get("DB_PWD", "password")
DB_USER = config.get("DB_USER", "user")
DB_HOST = config.get("DB_HOST", "0.0.0.0")

DB_URI = f"mariadb://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}"
