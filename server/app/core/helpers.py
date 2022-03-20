# Contains all helper functions, which is used to parse input and output
import enum
from typing import Optional

from fastapi.exceptions import HTTPException

from .config import get_app_settings


def ResponseModel(data: dict, message="Success"):
    """Standard template for a response returned by the server.

    Args:
            data (any): any data which is to be returned by the server.
            message (str, optional): Any additional message you want to send to the user.Defaults to "Success".

    Returns:
            [dict]: a dict containting {data, code:200, message}
    """
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, statuscode: int = 500, message: str = "Error"):
    """Standard template for a error returned by the server.

    Args:
            error (error): Helpful error message send to the user
            message (str): Any additional message you want to send to the user. Defaults to "Error"
            code (int, optional): Status Code of the error Message. Defaults to 500.

    Returns:
            [dict]: A dict containing {error, code, message}
    """
    errorMsg = {"error": error, "message": message}
    raise HTTPException(status_code=statuscode, detail=errorMsg)


def parseControllerResponse(data, statuscode: int, **kwargs):
    error = kwargs.get("error", None)
    message = kwargs.get("message", None)

    class Statuscode(enum.Enum):
        Success = 200
        BadRequest = 400  # wrong data
        Unauthorized = 401  # unauthenticated users
        Forbidden = 403  # authenticated, but not authorized to view the page
        NotFound = 404
        InternalServerError = 500
        DuplicateKey = 11000  # Mongo throws a 11000 error when there is a duplicate key

    # Generic error message for production env
    if get_app_settings().app_env != "dev" and statuscode == 500:
        error = "Something went wrong, try again later"

    resp = {
        "data": data,
        "statusCode": statuscode,
        "success": statuscode == 200,
        "statusMessage": (Statuscode(statuscode)).name,
        "error": error if error else None,
        "message": message if message else None,
    }

    # set duplicate key error status code to 400
    if resp["statusCode"] == 11000:
        resp["statusCode"] = 400

    return resp
