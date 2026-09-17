"""Small constructors shared by every contributor of the edge index."""

from __future__ import annotations

from typing import Any, Iterable

from sldb.store.edge_index.node_ids import tag_node_id
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def edge(source: str, target: str, relation: str, origin: str, **metadata: Any) -> EdgeRecord:
    """One edge whose metadata starts with where it came from (`origin`)."""
    return EdgeRecord(source=source, target=target, relation=relation, metadata={"origin": origin, **metadata})


def tag_nodes(tags: Iterable[str]) -> list[EdgeNodeRecord]:
    """The node of each tag, so every `tagged_as` target exists whoever contributed it."""
    return [EdgeNodeRecord(id=tag_node_id(t), node_type="semantic_tag", semantics={"tag": t}) for t in sorted(set(tags))]


def tagged_as(source: str, tags: Iterable[str]) -> list[EdgeRecord]:
    """`tagged_as` edges from `source` to each tag, in the order given."""
    return [edge(source, tag_node_id(t), "tagged_as", "structural") for t in tags]
