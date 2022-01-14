import os

from dotenv import dotenv_values

# TODO: add pydantic models to it


_dir_path = os.path.dirname(os.path.realpath(__file__))
_path = _dir_path + "/../../.env"
config = dotenv_values(_path)
# TODO: Clean this up
PORT = (
    int(config.get("PORT"))
    if config.get("PORT") != None and config.get("PORT").isdigit()
    else 8001
)
GRPC_SERVER_URI = config.get("PORT", "localhost:8000")
