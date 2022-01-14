import grpc  # type: ignore
import proto_build.DalalMessage_pb2_grpc as DalalMessage_pb2_grpc  # type: ignore
from proto_build.actions.Login_pb2 import LoginRequest  # type: ignore

# app = FastAPI()


if __name__ == "__main__":
    print("Trying to connect with grpc")
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
        action_stub = DalalMessage_pb2_grpc.DalalActionServiceStub(channel)
        login_req = LoginRequest(email="bot", password="bot")
        login_res = action_stub.Login(login_req)
        print("got the resp : ", login_res)
    except Exception as e:
        print("err : ", e)

# @app.get("/")
# def read_root():
#     return {"Dalal": "ToTheMoon"}
