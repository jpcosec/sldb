"""The relation type: what a verb is, declared as an sldb document (moved here from kgdb.models)."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from sldb.models.structured_doc import StructuredNLDoc


class RelationTypeDoc(StructuredNLDoc):
    """Declares one relation type: its name, which node classes it connects, its
    direction and cardinality, the predicate axis it answers, and a default
    condition every edge of this type inherits.

    The edge index reports any edge whose ``relation_type`` has no tracked
    RelationTypeDoc. The structural relations the index itself produces are shipped
    as RelationTypeDocs too (see ``sldb.models.builtin_relation_types``), so the
    graph is described entirely by documents.
    """

    __family__ = "relation"
    __semantics__ = {
        "type": ["relation", "type"],
        "layer": ["topology"],
    }
    __template__ = """---
name: ⸢rev•name⸥
direction: ⸢rev•direction⸥
cardinality: ⸢rev•cardinality⸥
axis: ⸢rev•axis⸥
source_types: ⸢rev,list•source_types⸥
target_types: ⸢rev,list•target_types⸥
condition: ⸢rev•condition⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    title: str = Field(description="Relation type title shown as the H1 heading.")
    name: str = Field(
        description="Vocabulary token for the relation type, e.g. booked_by or implements; the relation_type every edge carries."
    )
    direction: Literal["directed", "undirected"] = Field(
        default="directed",
        description="Directed edges read source->target only; undirected edges are materialized in both directions.",
    )
    cardinality: Literal["one_to_one", "one_to_many", "many_to_one", "many_to_many"] = Field(
        default="many_to_many",
        description="How many targets one source may have and how many sources one target may have; validated at ingest.",
    )
    axis: str = Field(
        default="",
        description="Predicate axis this relation answers (WHAT, WHY, HOW, WHERE, WHEN, PROVENANCE, ...); registered as an sldb predicate so prose links share the vocabulary.",
    )
    source_types: list[str] = Field(
        default_factory=list,
        description="Node classes allowed as source: model names (with inheritance) or index node types; empty means any.",
    )
    target_types: list[str] = Field(
        default_factory=list,
        description="Node classes allowed as target: model names (with inheritance) or index node types; empty means any.",
    )
    condition: str = Field(
        default="",
        description="sldb --where predicate every edge of this type inherits unless the RelationDoc overrides it; may name fields of the subject in braces, e.g. capacity >= {party_size}.",
    )
    description: str = Field(
        description="Markdown section describing the meaning and intended use of the relation type; it is the verb's motive in a lexicon."
    )
