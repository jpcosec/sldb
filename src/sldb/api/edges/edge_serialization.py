"""JSON projections of edge-index records (pydantic models) for API consumers."""

from __future__ import annotations

from typing import Any

from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord


def serialize_edge_records(records: list[EdgeRecord]) -> list[dict[str, Any]]:
    return [record.model_dump() for record in records]


def serialize_edge_record(record: EdgeRecord) -> dict[str, Any]:
    return record.model_dump()


def serialize_edge_node_records(records: list[EdgeNodeRecord]) -> list[dict[str, Any]]:
    return [record.model_dump() for record in records]


def serialize_edge_node_record(record: EdgeNodeRecord) -> dict[str, Any]:
    return record.model_dump()