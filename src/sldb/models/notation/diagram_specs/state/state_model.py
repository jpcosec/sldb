"""`state_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.base.doc_ref import DocRef


class StateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Stable state identifier referenced by transitions.")
    label: str = Field(description="Display label rendered for the state.")
    contains: list[str] | None = Field(default=None, description="Optional child states for composite (nested) states.")
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )
