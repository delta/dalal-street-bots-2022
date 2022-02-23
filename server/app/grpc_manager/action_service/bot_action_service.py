"""Class manager for all auth action service actions"""
import logging
from .base_action_service import BaseActionService

from proto_build.actions.CreateBot_pb2 import CreateBotRequest, CreateBotResponse


class BotActionService(BaseActionService):
    """Helper class to handle all bot-related grpc requests"""

    async def create_bot(self, bot_name: str) -> CreateBotResponse:
        """Create bot request"""

        createBotRequest = CreateBotRequest(bot_user_id=bot_name)

        try:
            resp: CreateBotResponse = await self.action_stub.CreateBot(
                createBotRequest,
                metadata=self.metadata.get_bot_meta_data(),
            )
            return resp
        except Exception as e:
            logging.error(e)
