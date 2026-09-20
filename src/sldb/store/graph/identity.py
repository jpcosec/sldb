"""The immutable base identity of a portable graph node."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.store.graph.vocabulary import VocabularyTerm


class SystemIdentity(BaseModel):
    """The unique identity and type of any node in the graph."""

    node_id: str = Field(description="A unique absolute identifier for the node.")
    node_type: VocabularyTerm = Field(description="The entity type token this node represents.")
