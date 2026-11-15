"""`semantic_metadata`."""

from __future__ import annotations

from pydantic import Field

from sldb.models.notation.diagram_specs.base.metadata import Metadata


class SemanticMetadata(Metadata):
    """Metadata supporting the 6D model for cross-ecosystem alignment."""

    who: str | None = Field(
        default=None, description="Who: Context actor or responsible entity."
    )
    what: str | None = Field(
        default=None, description="What: The object of the semantic relation."
    )
    where: str | None = Field(
        default=None, description="Where: Topology or persistence context."
    )
    when: str | None = Field(
        default=None, description="When: Temporal or phase context."
    )
    how: str | None = Field(
        default=None, description="How: Mechanical or technical context."
    )
    why: str | None = Field(
        default=None, description="Why: Rationale or business rule."
    )
