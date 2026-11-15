"""`diagram_store_ref`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DiagramStoreRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    project: str | None = None
    category: str | None = None
    type: str | None = None
    tags: list[str] = Field(default_factory=list)
