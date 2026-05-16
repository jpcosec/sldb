from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SourceSpan(BaseModel):
    line_start: int | None = Field(default=None, description="1-based start line.")
    line_end: int | None = Field(default=None, description="1-based end line.")


class SurfaceNode(BaseModel):
    kind: str = Field(description="Surface syntax node kind.")
    text: str = Field(default="", description="Original reversible text content.")
    span: SourceSpan = Field(default_factory=SourceSpan)
    children: list["SurfaceNode"] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentContext(BaseModel):
    physical: dict[str, Any] = Field(default_factory=dict)
    semantic: dict[str, Any] = Field(default_factory=dict)


class MeaningNode(BaseModel):
    kind: str = Field(description="Logical or operational node kind.")
    name: str = Field(description="Stable local identifier.")
    title: str | None = Field(default=None)
    model: str | None = Field(default=None)
    field_path: str | None = Field(default=None)
    value: Any = Field(default=None)
    owning_section: str | None = Field(
        default=None, description="Section path that owns this node."
    )
    span: SourceSpan = Field(default_factory=SourceSpan)
    children: list["MeaningNode"] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source: str = Field(description="Source node id.")
    target: str = Field(description="Target node id.")
    relation: str = Field(description="Typed relation between nodes.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphView(BaseModel):
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)


class SectionContextEntry(BaseModel):
    node_id: str = Field(description="Stable section node identifier.")
    path: str = Field(description="Hierarchical section path.")
    title: str = Field(description="Human section title.")
    breadcrumbs: list[str] = Field(default_factory=list)
    about: list[str] = Field(default_factory=list)
    semantic_tags: list[str] = Field(default_factory=list)
    span: SourceSpan = Field(default_factory=SourceSpan)


class DocumentIR(BaseModel):
    context: DocumentContext = Field(default_factory=DocumentContext)
    structure: list[MeaningNode] = Field(default_factory=list)
    nodes: list[MeaningNode] = Field(default_factory=list)
    surface: list[SurfaceNode] = Field(default_factory=list)
    graph: GraphView = Field(default_factory=GraphView)
    context_index: list[SectionContextEntry] = Field(default_factory=list)


SurfaceNode.model_rebuild()
MeaningNode.model_rebuild()
