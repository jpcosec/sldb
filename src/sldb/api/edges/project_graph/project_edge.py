"""An edge a project document declares."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProjectEdge(BaseModel):
    """A declared reference from one project node to another that exists."""

    model_config = ConfigDict(frozen=True)

    source_id: str = Field(description="Id of the declaring node.")
    target_id: str = Field(description="Id of the node the declaration names.")
    role: str = Field(description="The declaring field, or the role the declaration gives.")
    source_kind: str = Field(default="declared", description="How the edge is known.")
    confidence: str = Field(default="high", description="How sure the reader is of the edge.")
    provenance_path: str = Field(description="Path of the declaring document.")
    provenance_locator: str = Field(description="Where in it: `frontmatter` or `line:N:<section>`.")
    extractor: str = Field(description="Name and version of the reader.")
    record: bool | None = Field(default=None, description="True when the declaring document is an archived record.")

    def key(self) -> tuple[str, str, str, str]:
        """What makes two declarations the same edge, and the sort order of edges."""
        return (self.source_id, self.target_id, self.role, self.provenance_locator)

    def to_dict(self) -> dict[str, Any]:
        """The edge as plain data, without unset fields."""
        return self.model_dump(exclude_none=True)
