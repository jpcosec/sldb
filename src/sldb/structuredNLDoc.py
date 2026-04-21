from typing import TypeVar
from pydantic import BaseModel

class StructuredNLDoc(BaseModel):
    __template__: str = ""

M = TypeVar("M", bound="StructuredNLDoc")
