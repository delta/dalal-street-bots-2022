import logging
import os

import grpc
import proto_build.DalalMessage_pb2_grpc as DalalMessage_pb2_grpc
from core.config import get_app_settings


class GrpcManager:
    """This Class coordinates all the communication between our grpc-server and bots"""

    def __init__(self) -> None:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path + "/../../certs/grpc-server.crt"
            try:
                cert = open(path).read().encode("utf8")
            except Exception as e:
                # Unable to find the file, throw an error
                logging.error(f"Unable to open cert file from {path}")
            creds = grpc.aio.ssl_channel_credentials(cert)
            logging.info(
                f"Trying to connect to grpc server on port={get_app_settings().grpc_server_port}"
            )
            channel = grpc.secure_channel(
                "localhost:%d" % get_app_settings().grpc_server_port,
                creds,
                options=(
                    (
                        "grpc.ssl_target_name_override",
                        "localhost",
                    ),
                ),
            )
            self._channel = channel
            self.action_stub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
            self.stream_stub = DalalMessage_pb2_grpc.DalalStreamServiceStub(channel)
            logging.info("Successfully connected to the GRPC server")

        except Exception as e:
            logging.error("err : ", e)

    async def close_connection(self):
        """Closes the aio grpc connection"""
        # TODO: When intregrating with streams, need to gracefully close all streams before
        # closing the connection (Adding it here as a reminder)
        logging.info("Closing the connection with grpc server")
        await self._channel.close()
