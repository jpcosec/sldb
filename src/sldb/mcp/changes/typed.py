"""The union of typed changes and what is read off them."""

from __future__ import annotations

from typing import Annotated, Any, Union

from pydantic import Field

from sldb.mcp.changes.assert_edge import AssertEdge
from sldb.mcp.changes.create_document import CreateDocument
from sldb.mcp.changes.delete_document import DeleteDocument
from sldb.mcp.changes.retract_edge import RetractEdge
from sldb.mcp.changes.update_document import UpdateDocument
from sldb.mcp.mutability import model_level

#: The model of an authored edge (sldb.models.relation_doc).
EDGE_MODEL = "RelationDoc"

Change = Annotated[Union[CreateDocument, UpdateDocument, DeleteDocument, AssertEdge, RetractEdge], Field(discriminator="action")]


def model_of(change: CreateDocument | UpdateDocument | DeleteDocument | AssertEdge | RetractEdge) -> str:
    """The model of the document a change touches."""
    return getattr(change, "model", EDGE_MODEL)


def level_of(changes: list[Any]) -> int:
    """The write level a list of changes needs: the highest of its documents' models."""
    return max((model_level(model_of(c)) for c in changes), default=0)


def edge_payload(change: AssertEdge) -> dict[str, Any]:
    """The `RelationDoc` payload of an asserted edge."""
    title = change.title or f"{change.source} {change.relation_type} {change.target}"
    return {"title": title, "source_id": change.source, "target_id": change.target, "relation_type": change.relation_type, "condition": change.condition, "attributes": change.attributes, "notes": change.notes}
