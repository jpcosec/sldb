"""Tests for the content-blind relation layer models (docs.relation_models).

Covers: reversible-markdown roundtrip for RelationDoc and RelationTypeDoc, and
the Literal->enum schema descriptor fix in sldb.cli.serve.schema.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = str(Path(__file__).parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from docs.relation_models import RelationDoc, RelationTypeDoc  # noqa: E402
from sldb.cli.serve.schema import field_descriptors  # noqa: E402
from sldb.runtime.validation import (  # noqa: E402
    extract_model_data,
    render_model_markdown,
    validate_model_input_roundtrip,
)


def test_relation_instance_roundtrip():
    data = {
        "title": "step1 flows_to step2",
        "source_id": "step-1",
        "target_id": "step-2",
        "relation_type": "flows_to",
        "notes": "happy path",
    }
    md = render_model_markdown(RelationDoc, data)
    assert extract_model_data(RelationDoc, md) == data
    ok, _ = validate_model_input_roundtrip(RelationDoc, md)
    assert ok


def test_relation_type_roundtrip():
    data = {
        "title": "flows_to",
        "name": "flows_to",
        "direction": "directed",
        "cardinality": "many_to_many",
        "source_types": ["conversation-step"],
        "target_types": ["conversation-step"],
        "description": "Step A can transition to step B.",
    }
    md = render_model_markdown(RelationTypeDoc, data)
    assert extract_model_data(RelationTypeDoc, md) == data
    ok, _ = validate_model_input_roundtrip(RelationTypeDoc, md)
    assert ok


def test_relation_is_content_blind():
    """A relation instance carries only ids and a type token, no content."""
    fields = set(RelationDoc.model_fields)
    assert {"source_id", "target_id", "relation_type"} <= fields
    # no domain content fields leaked in
    assert "payload" not in fields
    assert "embedding" not in fields


def test_relation_type_literal_fields_expose_enum_schema():
    """serve /schema must surface Literal fields as enum with values (UI needs select)."""
    by_name = {f["name"]: f for f in field_descriptors(RelationTypeDoc)}
    assert by_name["direction"]["kind"] == "enum"
    assert by_name["direction"]["enum"] == ["directed", "undirected"]
    assert by_name["cardinality"]["kind"] == "enum"
    assert by_name["cardinality"]["enum"] == [
        "one_to_one",
        "one_to_many",
        "many_to_many",
    ]
