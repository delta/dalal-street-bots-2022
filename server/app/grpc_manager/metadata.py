"""A file containing all the metadata related logic"""
from typing import Any, List, Tuple
from core.config import get_app_settings


class MetadataMiddleware:
    """A class to initialize bot metadata, and fetch them.
    We pass a instance of it to all action and stream service to get the metadata."""

    bot_secret: str = get_app_settings().bot_secret
    admin_id: int = 0
    admin_session_id: str = ""

    def is_metadata_initialized(self) -> bool:
        """check to see if the metadata is initialized"""
        try:
            assert self.admin_id
            assert self.admin_session_id
            return True
        except AssertionError:
            return False

    def set_admin_bot_id(self, admin_id: int) -> None:
        """sets admin_id with the given id"""
        self.admin_id = admin_id

    def set_admin_session_id(self, session_id: str) -> None:
        """Sets the admin_session_id with the given id"""
        self.admin_session_id = session_id

    def set_meta_data(self, bot_id: int, session_id: str) -> None:
        """Sets the admin_session_id and admin_id with the given data"""
        self.set_admin_bot_id(bot_id)
        self.set_admin_session_id(session_id)

    def get_bot_meta_data(self) -> List[Tuple[str, str]]:
        """Returns bot metadata"""
        # BUG: low-priority.
        # We check for if both bot and admin metadata has been initialized
        # We only need to check one
        if not self.is_metadata_initialized:
            # TODO: create a type of error for it
            raise Exception("Metadata not initialied")
        return [("bot_secret", self.bot_secret), ("bot_user_id", str(self.admin_id))]

    def get_bot_meta_data_with_given_user_id(self, id: int) -> List[Tuple[str, str]]:
        """Returns bot meta data with the given bot id"""

        return [("bot_secret", self.bot_secret), ("bot_user_id", str(id))]

    def get_admin_meta_data(self) -> List[Tuple[str, str]]:
        "returns a admin metadata"
        if not self.is_metadata_initialized:
            # TODO: create a type of error for it
            raise Exception("Metadata not initialied")
        return [
            ("sessionid", self.admin_session_id),
            ("bot_user_id", str(self.admin_id)),
        ]
