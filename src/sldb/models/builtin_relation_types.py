"""The relation types the edge index itself produces, shipped as RelationTypeDoc payloads
(moved here from kgdb.models.builtin).

`sldb.api.init_relations` writes each of these as a tracked document in the store so that
every structural edge of the index has a type, like any authored edge. Node classes here
are index node types (``sldb_store``, ``sldb_model``, ...); authored relation types use
model names instead.
"""

from __future__ import annotations

from typing import Any

# (name, axis, cardinality, source_types, target_types, description)
_TABLE: list[tuple[str, str, str, list[str], list[str], str]] = [
    ("has_model", "WHAT", "one_to_many", ["sldb_store"], ["sldb_model"], "The store registers this model."),
    ("has_document", "WHAT", "one_to_many", ["sldb_model"], [], "The model has this document as an instance."),
    ("has_section", "WHERE", "one_to_many", [], ["sldb_section"], "The document contains this section."),
    ("tagged_as", "WHAT", "many_to_many", [], ["semantic_tag"], "The model, document or section carries this semantic tag."),
    ("semantic_parent", "WHAT", "many_to_many", ["semantic_tag"], ["semantic_tag"], "This tag is a child of that tag in the semantic DAG."),
    ("semantic_equivalent", "WHAT", "many_to_many", ["semantic_tag"], ["semantic_tag"], "This local tag maps to that global tag across linked stores."),
    ("has_field", "WHAT", "one_to_many", ["sldb_model"], ["sldb_field"], "The model declares this field; the field node carries its type and description."),
    ("extends", "WHAT", "many_to_many", ["sldb_model"], ["sldb_model"], "The model inherits from that model (base_models); instances of the source are instances of the target."),
    ("applies_to_source", "WHAT", "many_to_many", ["relation_type"], ["sldb_model"], "Instances of this model may be the source of edges of this relation type: the verbs a class can be subject of."),
    ("applies_to_target", "WHAT", "many_to_many", ["relation_type"], ["sldb_model"], "Instances of this model may be the target of edges of this relation type."),
    ("names", "WHAT", "many_to_many", ["anchor"], [], "The anchor (an alias word) names this model, field, relation type or document."),
]
_KEYS = ("name", "axis", "cardinality", "source_types", "target_types", "description")

BUILTIN_RELATION_TYPES: list[dict[str, Any]] = [dict(zip(_KEYS, row)) for row in _TABLE]


def builtin_payload(spec: dict[str, Any]) -> dict[str, Any]:
    """Full RelationTypeDoc payload for one builtin spec."""
    own = {key: spec[key] for key in ("name", "cardinality", "axis", "description")}
    ends = {"source_types": list(spec["source_types"]), "target_types": list(spec["target_types"])}
    return {"title": spec["name"], "direction": "directed", "condition": "", **own, **ends}


def builtin_doc_name(spec: dict[str, Any]) -> str:
    """Name the builtin relation type is tracked under."""
    return f"reltype-{spec['name']}"
