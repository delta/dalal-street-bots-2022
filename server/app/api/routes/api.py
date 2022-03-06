import logging
from fastapi import APIRouter, Body, Depends

from ..schemas.api import CreateBotRequest
from core.dependencies.grpc import get_grpc_client_stub
from core.dependencies.database import get_connection, Cursor
from grpc_manager.grpc_api import GrpcManager
from db.crud import bots, bot_types

router = APIRouter()


@router.post("/bot", response_description="Creates a new bot with the given details")
async def create_new_bot(
    create_bot_request: CreateBotRequest = Body(...),
    grpc_manager: GrpcManager = Depends(get_grpc_client_stub),
    conn: Cursor = Depends(get_connection),
):
    """Creates a bot in grpc server, and makes a details of it in db
    - Returns True if the bot is created successfully, else is returns false"""

    try:
        logging.info(f"trying to create a bot with {create_bot_request.dict()}")


        resp, err = await grpc_manager.bot_action_service.create_bot(
            create_bot_request.name
        )

        assert not err
        
        # if condn shd always pass, adding this to bypass mypy error
        server_bot_id = resp.user.id if resp else 0

        resp, err = await bots.create_bot(
            conn,
            bot_type=create_bot_request.bot_type,
            name=create_bot_request.name,
            server_bot_id=server_bot_id,
        )

        assert not err
        
        return resp

    except AssertionError:
        logging.error(
            f"Unable to create bot with {create_bot_request.dict()} due to {err}"
        )
        return False
