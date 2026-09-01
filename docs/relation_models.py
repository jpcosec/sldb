"""Content-blind relation layer models.

Per RELATION_MODEL_LAYER_SPEC: a relation is not a hidden field inside content;
it is its own content-blind model authored in sldb. Two levels:

- ``RelationTypeDoc`` (spec): defines what a relation type IS -- valid endpoints,
  direction, cardinality. It is content, so it lives in sldb.
- ``RelationDoc`` (instance): a concrete authored edge A->B of a given type. Also
  an sldb document, validated against its type.

Both are plain ``StructuredNLDoc`` subclasses. sldb stays the single authoring
layer; kgdb becomes a pure assembler that consumes these instead of re-parsing
text fields on content models.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from sldb import StructuredNLDoc


class RelationTypeDoc(StructuredNLDoc):
    """Spec model: defines a relation type's contract (content-blind)."""

    __family__ = "relation"
    __semantics__ = {
        "type": ["relation", "type"],
        "layer": ["topology"],
    }
    __template__ = """---
name: ⸢rev•name⸥
direction: ⸢rev•direction⸥
cardinality: ⸢rev•cardinality⸥
source_types: ⸢rev,list•source_types⸥
target_types: ⸢rev,list•target_types⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
"""

    title: str = Field(description="Relation type title shown as the H1 heading.")
    name: str = Field(
        description="Vocabulary token for the relation type, e.g. flows_to or grounded_by."
    )
    direction: Literal["directed", "undirected"] = Field(
        description="Whether edges of this type are directed (source->target) or undirected."
    )
    cardinality: Literal["one_to_one", "one_to_many", "many_to_many"] = Field(
        default="many_to_many",
        description="Allowed cardinality between source and target endpoints.",
    )
    source_types: list[str] = Field(
        default_factory=list,
        description="Allowed source node types; empty means any type is accepted.",
    )
    target_types: list[str] = Field(
        default_factory=list,
        description="Allowed target node types; empty means any type is accepted.",
    )
    description: str = Field(
        description="Markdown section describing the meaning and intended use of the relation type."
    )


class RelationDoc(StructuredNLDoc):
    """Instance model: one authored edge A->B of a given relation type."""

    __family__ = "relation"
    __semantics__ = {
        "type": ["relation", "instance"],
        "layer": ["topology"],
    }
    __template__ = """---
source_id: ⸢rev•source_id⸥
target_id: ⸢rev•target_id⸥
relation_type: ⸢rev•relation_type⸥
---

# ⸢rev•title⸥

## Notes

⸢rev,markdown•notes⸥
"""

    title: str = Field(description="Relation instance title shown as the H1 heading.")
    source_id: str = Field(
        description="Id of the source node this relation originates from."
    )
    target_id: str = Field(
        description="Id of the target node this relation points to."
    )
    relation_type: str = Field(
        description="Vocabulary token naming the relation type, matching a RelationTypeDoc name."
    )
    notes: str = Field(
        default="",
        description="Optional markdown notes about this specific authored edge.",
    )
