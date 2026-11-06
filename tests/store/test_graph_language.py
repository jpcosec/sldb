"""The structured query language, with the two defects of its first version fixed."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb.store.graph.language import RelationFilter, StructuredQuery

FIXTURE = Path(__file__).resolve().parents[2] / "contracts" / "queries" / "sldb"


def test_example_queries_parse():
    for path in sorted(FIXTURE.glob("*.json")):
        StructuredQuery.model_validate(json.loads(path.read_text(encoding="utf-8")))


def test_a_facet_filter_with_the_old_conditions_key_is_rejected_naming_it():
    query = {"filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "x"}]}]}
    with pytest.raises(ValidationError, match="conditions"):
        StructuredQuery.model_validate(query)


def test_relation_filter_declares_direction():
    assert RelationFilter().direction == "both"
    assert RelationFilter(direction="incoming").direction == "incoming"
