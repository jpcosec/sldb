"""`component_data`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.component.edge_model import EdgeModel
from sldb.models.notation.diagram_specs.component.node_model import NodeModel


class ComponentData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nodes: dict[str, NodeModel] = Field(
        description="Component nodes keyed by identifier."
    )
    edges: list[EdgeModel] = Field(
        default_factory=list,
        description="Relationships between the declared component nodes.",
    )
