"""Class manager for all auth action service actions"""

from datetime import datetime
import logging
from .base_action_service import BaseActionService

from proto_build.actions.Login_pb2 import LoginRequest, LoginResponse


class AuthActionService(BaseActionService):
    """Helper class to handle all auth related validations"""

    async def login(self, email: str, password: str):
        """Login request"""

        loginRequest = LoginRequest(email=email, password=password)

        response: LoginResponse = await self.action_stub.Login(loginRequest)

        # logging.info(f"got the response  in {(end-start).total_seconds()}")
        return response
