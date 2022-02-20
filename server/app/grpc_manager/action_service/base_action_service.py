from grpc.aio import Channel
from proto_build.DalalMessage_pb2_grpc import DalalActionService
from core.config import get_app_settings


class BaseActionService:
    """Base class for action service, all the other action service
    will be a child of this class"""

    def __init__(
        self, channel: Channel, action_stub: DalalActionService, *args, **kwargs
    ):
        self.channel = channel
        self.action_stub = action_stub
    
    def getMd(self,botId: int):
        """Metadata for all bot requests. Includes bot secret in the request for creating fake session in the server"""
        bot_secret=get_app_settings().bots_secret

        return [("bot_secret", bot_secret),("bot_user_id", botId)]
