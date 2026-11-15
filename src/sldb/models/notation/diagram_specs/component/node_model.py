"""`node_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.base.doc_ref import DocRef


class NodeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str | None = Field(
        default=None, description="Optional display name for the component node."
    )
    kind: str = Field(
        default="core", description="Semantic category for the component."
    )
    contains: list[str] = Field(
        default_factory=list,
        description="Identifiers of nested components contained by this node.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )
    href: str | None = Field(
        default=None,
        description="Optional URL the node opens when clicked; the mermaid renderer emits it as a `click` line.",
    )
