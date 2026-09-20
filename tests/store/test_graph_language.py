"""The structured query language, ported from kgdb with the two known defects fixed."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.store.graph.language import FieldCondition, RelationFilter, StructuredQuery

FIXTURE = Path(__file__).resolve().parents[2] / "contracts" / "queries" / "sldb"


def test_example_queries_parse():
    for path in sorted(FIXTURE.glob("*.json")):
        StructuredQuery.model_validate(json.loads(path.read_text(encoding="utf-8")))


def test_field_condition_accepts_all_eight_operators():
    for op in ("eq", "ne", "is_null", "is_not_null", "contains", "gt", "lt", "starts_with"):
        FieldCondition(field="name", op=op, value="x")


def test_relation_filter_declares_direction():
    assert RelationFilter().direction == "both"
    assert RelationFilter(direction="incoming").direction == "incoming"
