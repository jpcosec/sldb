"""Assert an authored edge."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from sldb.mcp.changes.base import _Change


class AssertEdge(_Change):
    """Assert an authored edge: a `RelationDoc` source -[relation_type]-> target."""

    action: Literal["assert_edge"]
    name: str = Field(description="The RelationDoc's name, unique in the store.")
    source: str = Field(description="Export id of the source document (`Model:name`, `alias:Model:name` for a linked store).")
    target: str = Field(description="Export id of the target document.")
    relation_type: str = Field(description="The name of a tracked RelationTypeDoc.")
    title: str | None = Field(default=None, description="The RelationDoc's title; omitted, `<source> <relation_type> <target>`.")
    condition: str = Field(default="", description="A predicate for this edge only; empty inherits the type's condition.")
    attributes: dict[str, Any] = Field(default_factory=dict)
    notes: str = Field(default="")
    path: str | None = Field(default=None, description="Markdown path relative to the project root; omitted, RelationDoc's default directory.")
