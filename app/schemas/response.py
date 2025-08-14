from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class ResponseBase(BaseModel):
    success: bool
    message: Optional[str] = None


class ResponseSingle(ResponseBase, Generic[T]):
    data: Optional[T] = None


class ResponseList(ResponseBase, Generic[T]):
    data: List[T] = []
    total: Optional[int] = None
    page: Optional[int] = None
    size: Optional[int] = None


class ResponseError(ResponseBase):
    success: bool = False
    errors: List[ErrorDetail] = []
