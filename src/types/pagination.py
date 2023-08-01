from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import List, TypeVar
from typing import Generic

T = TypeVar("T")

class ListRequest(BaseModel):
  page: int
  count: int

class ListResponse(GenericModel, Generic[T]):
  count: int
  page_number: int
  is_next: bool
  data: List[T]
