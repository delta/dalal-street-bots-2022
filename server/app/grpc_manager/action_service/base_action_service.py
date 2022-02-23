from importlib.metadata import metadata
from grpc.aio import Channel
from proto_build.DalalMessage_pb2_grpc import DalalActionService
from ..metadata import MetadataMiddleware


class BaseActionService:
    """Base class for action service, all the other action service
    will be a child of this class"""

    def __init__(
        self,
        channel: Channel,
        action_stub: DalalActionService,
        metadata: MetadataMiddleware,
        *args,
        **kwargs,
    ):
        self.channel = channel
        self.action_stub = action_stub
        self.metadata = metadata

    def get_bot_meta_data(self):
        """Gets bot metadata"""
        return self.metadata.get_bot_meta_data()

    def get_admin_meta_data(self):
        """Gets admin metadata"""
        return self.metadata.get_admin_meta_data()
