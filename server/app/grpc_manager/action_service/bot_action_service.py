"""Class manager for all auth action service actions"""

from datetime import datetime
import logging
from .base_action_service import BaseActionService

from proto_build.actions.CreateBot_pb2 import CreateBotRequest, CreateBotResponse


class BotActionService(BaseActionService):
    """Helper class to handle all bot-related grpc requests"""

    async def create_bot(self, bot_user_id: int) -> CreateBotResponse:
        """Create bot request"""

        createBotRequest = CreateBotRequest(bot_user_id=str(bot_user_id))

        resp: CreateBotResponse = await createBotRequest

        return resp
