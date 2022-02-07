from datetime import datetime

from pydantic import BaseModel


class TimestampInDBPlugin(BaseModel):
    """Plugin for db models for created_at and updated_at"""

    created_at: datetime
    updated_at: datetime
