"""Class manager for all auth action service actions"""
import logging
from typing import Tuple, Union
from .base_action_service import BaseActionService

from proto_build.actions.CreateBot_pb2 import CreateBotRequest, CreateBotResponse


class BotActionService(BaseActionService):
    """Helper class to handle all bot-related grpc requests"""

    async def create_bot(
        self, bot_name: str
    ) -> Tuple[Union[CreateBotResponse, None], Union[Exception, None]]:
        """Create bot request"""

        logging.info(f"trying to create a bot wih name={bot_name}")
        try:
            createBotRequest = CreateBotRequest(bot_user_id=bot_name)
            resp: CreateBotResponse = await self.action_stub.CreateBot(
                createBotRequest,
                metadata=self.metadata.get_bot_meta_data(),
            )

            if resp.status_code > 0:
                # Some error occurred, sending resp response and status_message as response
                logging.info(
                    f"creating a bot with name={bot_name} failed due to={resp.status_message}"
                )
                return resp, resp.status_message

            logging.info(f"Successfully created a bot with name={bot_name}")
            return resp, None
        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e
        except Exception as e:
            logging.error(
                f"Unable to create a bot with name={bot_name} due to {e}", exc_info=True
            )
