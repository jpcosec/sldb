"""Neighborhood traversal over the edge index's _out/_in maps."""

from __future__ import annotations

from sldb.store.graph import collect_neighborhood, collect_neighborhood_by_direction
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.models import EdgeNodeRecord, EdgeRecord

A, B, C, D = ("sldb://document/a", "sldb://document/b", "sldb://document/c", "sldb://document/d")


def _index() -> EdgeIndex:
    nodes = {nid: EdgeNodeRecord(id=nid, node_type="concept") for nid in (A, B, C, D)}
    edges = [
        EdgeRecord(source=A, target=B, relation="r"),
        EdgeRecord(source=B, target=C, relation="r"),
        EdgeRecord(source=A, target=D, relation="r"),
    ]
    return EdgeIndex(nodes=nodes, edges=edges)


def test_collect_neighborhood_includes_seeds():
    assert collect_neighborhood(_index(), [A], 1) == {A, B, D}


def test_collect_neighborhood_by_direction_outgoing():
    assert collect_neighborhood_by_direction(_index(), {A}, 1, "outgoing") == {B, D}


def test_collect_neighborhood_by_direction_incoming():
    assert collect_neighborhood_by_direction(_index(), {C}, 1, "incoming") == {B}


def test_collect_neighborhood_depth_two():
    assert collect_neighborhood(_index(), [A], 2) == {A, B, C, D}
