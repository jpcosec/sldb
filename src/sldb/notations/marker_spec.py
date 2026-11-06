"""`MarkerSpec`: una marca que apunta a un elemento sin ser su glifo."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator

from sldb.notations.where_check import _check_where


class MarkerSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    shape: str
    model: str
    where: str = ""

    @field_validator("where")
    @classmethod
    def _where(cls, v: str) -> str:
        _check_where(v)
        return v
