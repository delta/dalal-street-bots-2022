import logging
from fastapi import APIRouter, Body, Depends, HTTPException, Response

from starlette.status import HTTP_400_BAD_REQUEST

from core.dependencies.grpc import get_grpc_client_stub
from core.auth import auth_handler
from core.helpers import ResponseModel

# from core.dependencies.database import get_connection, Cursor
from grpc_manager.grpc_api import GrpcManager
from db.crud import bots, bot_types
from ..schemas.auth import LoginRequest, LoginResponse
from ..schemas.responses import GenericResponseSchema

from ..resources import strings

router = APIRouter()


@router.post(
    "/login",
    response_description="checks user credentials and create a account",
    name="auth:login",
)
async def login(
    response: Response,
    login_request: LoginRequest = Body(...),
    grpc_manager: GrpcManager = Depends(get_grpc_client_stub),
) -> LoginResponse:
    logging.info("trying to log in user")
    resp, err = await grpc_manager.auth_action_service.login(
        login_request.email, login_request.password
    )

    invalid_credentials_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST, detail=strings.UNAUTHENTICATED_ERROR
    )

    if not resp or err:
        logging.error(f"Unable to log into dalal {err}")
        raise invalid_credentials_error

    if not resp.user.is_admin:
        logging.error("The user logging in is not admin")
        raise invalid_credentials_error

    # saving admin meta-data to bot manager
    grpc_manager.metadata.set_meta_data(bot_id=resp.user.id, session_id=resp.session_id)

    token = auth_handler.encode_token(resp.user.id)

    logging.info("successfully logged in user")
    return LoginResponse(success=True, token=token)


@router.get("/me")
async def hello(user_id=Depends(auth_handler.auth_wrapper)):
    return "Hello world"
