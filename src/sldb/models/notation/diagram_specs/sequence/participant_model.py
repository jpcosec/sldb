"""`participant_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.base.doc_ref import DocRef


class ParticipantModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Unique participant identifier referenced by messages.")
    kind: str = Field(
        default="component",
        description="Semantic participant kind used for styling or grouping.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )
