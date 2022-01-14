import grpc
import proto_build.DalalMessage_pb2_grpc as DalalMessage_pb2_grpc


class GrpcManager:
    """This Class coordinates all the communication between our grpc-server and bots"""

    def __init__(self) -> None:
        try:
            cert = open("grpc-server.crt").read().encode("utf8")
            creds = grpc.ssl_channel_credentials(cert)
            channel = grpc.secure_channel(
                "localhost:8000",
                creds,
                options=(
                    (
                        "grpc.ssl_target_name_override",
                        "localhost",
                    ),
                ),
            )
            self.action_stub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
        except Exception as e:
            print("err : ", e)
