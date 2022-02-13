import os
import time
import traceback

import grpc
import proto_build.DalalMessage_pb2_grpc as DalalMessage_pb2_grpc
from proto_build.actions.Login_pb2 import LoginRequest, LoginResponse
from core.config import get_app_settings
import logging


async def call_login_as_coroutine():
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = dir_path + "/../../certs/grpc-server.crt"
        cert = open(path).read().encode("utf8")
        creds = grpc.ssl_channel_credentials(cert)
        logging.info(
            f"Connecting to grpc server at: {get_app_settings().grpc_server_uri}"
        )
        channel = grpc.aio.secure_channel(
            "localhost:8000",
            creds,
            options=(
                (
                    "grpc.ssl_target_name_override",
                    "localhost",
                ),
            ),
        )
        action_stub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
        stream_stub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)
        # time.sleep(10)
        newLoginRequest = LoginRequest(email="email@email.com", password="password")
        try:
            response = await action_stub.Login(newLoginRequest)
            print(response)
        except Exception as e:
            print(traceback.format_tb(e.__traceback__))
            print(e)

    except Exception as e:
        print("err : ", e)


class GrpcManager:
    """This Class coordinates all the communication between our grpc-server and bots"""

    def __init__(self) -> None:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path + "/../../certs/grpc-server.crt"
            cert = open(path).read().encode("utf8")
            creds = grpc.ssl_channel_credentials(cert)
            logging.info(
                f"Connecting to grpc server at: {get_app_settings().grpc_server_uri}"
            )
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

        except Exception as e:
            print("err : ", e)

    async def login_request(self):
        newLoginRequest = LoginRequest(email="email@email.com", password="password")
        try:
            response = await self.action_stub.Login(newLoginRequest)
            print(response)
        except Exception as e:
            print(traceback.format_tb(e.__traceback__))
            print(e)
