"""`reflection_ir`."""

from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.reflection.reflection_edge import ReflectionEdge
from sldb.models.notation.diagram_specs.reflection.reflection_node import ReflectionNode


class ReflectionIR(BaseModel):
    """Semantic Intermediate Representation for reflection and enforcement."""

    model_config = ConfigDict(extra="forbid")

    nodes: Dict[str, ReflectionNode] = Field(
        description="Reflection nodes keyed by their stable identifier."
    )
    edges: List[ReflectionEdge] = Field(
        default_factory=list, description="Relationships between the reflection nodes."
    )
