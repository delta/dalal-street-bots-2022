from typing import Any

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
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._channel = channel
        self._action_stub = action_stub
        self._metadata = metadata
