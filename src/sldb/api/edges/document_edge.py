"""One document-to-document edge, as a UI draws it."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DocumentEdge(BaseModel):
    """An edge whose two ends are documents, ids as `Model:name`."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="The RelationDoc name for authored edges, else `relation:source>target`.")
    source: str = Field(description="Export id `Model:name` of the document the edge leaves from.")
    target: str = Field(description="Export id `Model:name` of the document the edge points at.")
    type: str = Field(description="Relation type token (`motiva`, `references`...).")
    origin: str = Field(description="The edge's `metadata.origin`: relation_doc, schema, structural.")
    relation_doc: str | None = Field(default=None, serialization_alias="relationDoc", description="Name of the authoring RelationDoc when origin is relation_doc.")
