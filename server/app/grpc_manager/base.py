import os

import grpc
import proto_build.DalalMessage_pb2_grpc as DalalMessage_pb2_grpc

from ..core.config import GRPC_SERVER_URI


class GrpcManager:
    """This Class coordinates all the communication between our grpc-server and bots"""

    def __init__(self) -> None:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path + "/../../certs/grpc-server.crt"
            cert = open(path).read().encode("utf8")
            creds = grpc.ssl_channel_credentials(cert)
            channel = grpc.secure_channel(
                GRPC_SERVER_URI,
                creds,
                options=(
                    (
                        "grpc.ssl_target_name_override",
                        "localhost",
                    ),
                ),
            )
            self.action_stub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
            self.stream_stub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)

        except Exception as e:
            print("err : ", e)
