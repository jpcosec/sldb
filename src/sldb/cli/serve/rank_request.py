"""The query string of GET /corpus/rank, validated once at the HTTP boundary."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RankRequest(BaseModel):
    """`q` plus the optional knobs; `among` arrives as a comma-separated string."""

    model_config = ConfigDict(extra="ignore")

    q: str = Field(min_length=1)
    k: int = Field(default=5, ge=1)
    threshold: float = 0.0
    among: list[str] | None = None
    fields: bool = False
    refresh: bool = False

    @field_validator("among", mode="before")
    @classmethod
    def split_among(cls, value: Any) -> Any:
        """`a,b` becomes `["a", "b"]`; blank items are dropped and an empty list means no filter."""
        if not isinstance(value, str):
            return value
        return [item for item in value.split(",") if item.strip()] or None
