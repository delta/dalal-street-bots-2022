from typing import Union
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "ajith@gmail.com",
                "password": "password",
            }
        }


class LoginResponse(BaseModel):
    success: bool = Field(...)
