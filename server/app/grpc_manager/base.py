import os

import grpc
import proto_build.DalalMessage_pb2_grpc as DalalMessage_pb2_grpc


class GrpcManager:
    """This Class coordinates all the communication between our grpc-server and bots"""

    def __init__(self) -> None:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path + "/../../certs/grpc-server.crt"
            cert = open(path).read().encode("utf8")
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
            self.stream_stub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)

            # test to see if we are able to ping the server
            # TODO: create a ping method in server to test if the connection is working
            # login_req = LoginRequest(email="bot", password="bot")
            # login_res = self.action_stub.Login(login_req)
            # print("login response", login_res)
        except Exception as e:
            print("err : ", e)
