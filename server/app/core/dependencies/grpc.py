"""manages dependencies for grpc_manager"""

from fastapi import Request
from grpc_manager.grpc_api import GrpcManager


def get_grpc_client_stub(request: Request) -> GrpcManager:
    """Returns a grpc client stub connection"""
    return request.app.state.grpc
