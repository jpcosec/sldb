"""A declared target that resolves to no project node."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MissingProjectTarget(BaseModel):
    """A dangling declaration: the finding `graph missing` reports."""

    model_config = ConfigDict(frozen=True)

    source_id: str = Field(description="Id of the declaring node.")
    target_id: str = Field(description="Id the declaration names, which no node has.")
    provenance_path: str = Field(description="Path of the declaring document.")
    provenance_locator: str = Field(description="Where in it the declaration sits.")
    reason: str = Field(description="Why the target is missing.")
    extractor: str = Field(description="Name and version of the reader.")
    record: bool | None = Field(default=None, description="True when the declaring document is history.")

    def key(self) -> tuple[str, str, str]:
        """What makes two findings the same, and their sort order."""
        return (self.source_id, self.target_id, self.provenance_locator)

    def to_dict(self) -> dict[str, Any]:
        """The finding as plain data, without unset fields."""
        return self.model_dump(exclude_none=True)
