from grpc.aio import Channel
from proto_build.DalalMessage_pb2_grpc import DalalActionService


class BaseActionService:
    """Base class for action service, all the other action service
    will be a child of this class"""

    def __init__(
        self, channel: Channel, action_stub: DalalActionService, *args, **kwargs
    ):
        self.channel = channel
        self.action_stub = action_stub
