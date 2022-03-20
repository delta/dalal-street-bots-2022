from typing import Union
from pydantic import BaseModel, Field


class CreateBotRequest(BaseModel):
    """Model for validating create new bot request"""

    name: str = Field(...)
    bot_type: Union[int, str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "example_bot_1",
                "bot_type": "news_bot",
            }
        }
