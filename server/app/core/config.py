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
GRPC_SERVER_URI = config.get("PORT", "localhost:8000")
