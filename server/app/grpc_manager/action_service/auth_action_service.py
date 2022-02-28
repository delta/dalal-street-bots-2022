"""Class manager for all auth action service actions"""

import logging
from typing import Tuple, Union

from proto_build.actions.Login_pb2 import LoginRequest, LoginResponse

from .base_action_service import BaseActionService


class AuthActionService(BaseActionService):
    """Helper class to handle all auth related validations"""

    async def login(
        self, email: str, password: str
    ) -> Tuple[Union[LoginResponse, None], Union[Exception, None]]:
        """Login request"""

        try:
            loginRequest = LoginRequest(email=email, password=password)

            resp: LoginResponse = await self.action_stub.Login(loginRequest)

            if resp.status_code > 0:
                # Some error occurred, sending resp response
                # and status_message as response
                logging.info(
                    "unable to login, got grpc_error failed"
                    f"due to={resp.status_message}"
                )
                return resp, resp.status_message
            # logging.info(f"got the response  in {(end-start).total_seconds()}")
            return resp, None
        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e
        except Exception as e:
            logging.error(f"Unable to login  due to {e}", exc_info=True)
            return None, e
