"""`deployment_node_model`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.base.doc_ref import DocRef


class DeploymentNodeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str | None = Field(
        default=None, description="Optional display name for the deployment node."
    )
    kind: str = Field(
        default="server",
        description="Semantic infrastructure kind, such as server or browser.",
    )
    contains: list[str] = Field(
        default_factory=list,
        description="Artifact or node identifiers hosted within this deployment node. Nodes nest (VPC > subnet > cluster > service): a node has at most one parent and containment has no cycles.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )
