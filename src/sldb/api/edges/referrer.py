"""One incoming reference to a document or to a project graph node (GD22)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Referrer(BaseModel):
    """Where one reference to the target is written: a declared field of a tracked document
    (`origin: schema`) or a mention a `MentionPattern` captured in prose (`origin: mention`)."""

    model_config = ConfigDict(frozen=True)

    source: str = Field(description="Export id `Model:name` of the referring document, or the project-relative path of the file holding the mention.")
    field: str | None = Field(default=None, description="The declared field holding the reference; None for a mention.")
    index: int | None = Field(default=None, description="Position of the reference in a list field; None for a scalar field or a mention.")
    location: str | None = Field(default=None, description="`path:line` of a mention; None for a field.")
    origin: str = Field(description="`schema` (a field the model declares, read from the edge index) or `mention` (prose, read from the project graph).")

    def to_dict(self) -> dict[str, Any]:
        """The reference as plain data, every key present."""
        return self.model_dump()
