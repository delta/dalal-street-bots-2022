from pydantic import Field
from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar

DataT = TypeVar("DataT")


class GenericResponseSchema(GenericModel, Generic[DataT]):
    # Generic Response Model
    code: int = Field(...)
    message: str = Field(...)

    data: Optional[DataT]
    error: Optional[dict]
