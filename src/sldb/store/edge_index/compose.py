"""Shards -> one EdgeIndex: every store's contributions merged (the same node id is one node,
the first contributor's), the cross-document rules applied. Composed once per state of the
shards: the result is kept while no shard file, and no store index, has moved."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.store.edge_index.composition_targets import resolve_composition_edges
from sldb.store.edge_index.doc_anchor_states import with_anchor_states
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.federation import federated_stores, qualify
from sldb.store.edge_index.live_stale import ModelTypeOf, live_stale
from sldb.store.edge_index.resolve import resolve_edges_reporting
from sldb.store.edge_index.shard_reading import read_store_contributions
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io import load_store_index
from sldb.store.models import EdgeContribution, EdgeNodeRecord, EdgeRecord, ModelEdges

_COMPOSED: dict[tuple, tuple[tuple, EdgeIndex]] = {}


def compose_edge_index(store_path: Path, include_linked: bool = True, exclude_tags: Iterable[str] = (), model_type_of: ModelTypeOf | None = None) -> EdgeIndex:
    """The store's edge index, read from its shards (never rebuilt here).

    Args:
        store_path: The store's `.sldb` directory.
        include_linked: Also read the linked stores' indexes, their ids qualified by name.
        exclude_tags: Documents carrying one of these tags are left out (their nodes, their
            sections, their edges); the index itself holds everything.
        model_type_of: Loads a model class (`(model_ref, project_root) -> class | None`), so
            `stale` also names documents built under another contract of their model, and a
            document node's payload gains `<field>__anchor_state` for each of its model's
            `__doc_anchors__` (GO07: on copies, never in a shard; without it, none).

    Returns:
        The composed index; shared between callers, so treat it as read-only. Its `stale` is
        checked on every call against the files on disk (`live_stale`), not only the shards.
    """
    stores = federated_stores(Path(store_path), include_linked)
    key = (str(stores[0][0]), include_linked, frozenset(exclude_tags), model_type_of)
    signature = tuple(shards_signature(path) for path, _ in stores)
    hit = _COMPOSED.get(key)
    if hit is None or hit[0] != signature:
        hit = _COMPOSED[key] = (signature, _compose(stores, frozenset(exclude_tags), model_type_of))
    return _with_live_stale(hit[1], stores, model_type_of)


def _with_live_stale(index: EdgeIndex, stores: list[tuple[Path, str | None]], model_type_of: ModelTypeOf | None) -> EdgeIndex:
    moved, known = [f"{name}:{e}" if name else e for path, name in stores for e in live_stale(path, model_type_of)], set(index.stale)
    extra = [e for e in dict.fromkeys(moved) if e not in known]
    return index.model_copy(update={"stale": index.stale + extra}) if extra else index


def invalidate_composed_edge_indexes() -> None:
    """Forget every composed index (tests, or a caller that rewrote shards by hand)."""
    _COMPOSED.clear()


def _compose(stores: list[tuple[Path, str | None]], exclude_tags: frozenset[str], model_type_of: ModelTypeOf | None) -> EdgeIndex:
    nodes: dict[str, EdgeNodeRecord] = {}
    edges: list[EdgeRecord] = []
    stale: list[str] = []
    fields: dict[str, list[str]] = {}
    for path, name in stores:
        stale += _merge_store(path, name, exclude_tags, nodes, edges, fields)
    nodes = with_anchor_states(nodes, [path for path, _ in stores], model_type_of, fields)
    kept, problems, unresolved = resolve_edges_reporting(nodes, resolve_composition_edges(nodes, edges))
    return EdgeIndex(nodes=nodes, edges=kept, problems=problems, stale=stale, unresolved_references=unresolved, payload_fields=fields)


def _merge_store(path: Path, name: str | None, exclude_tags: frozenset[str], nodes: dict, edges: list[EdgeRecord], fields: dict[str, list[str]]) -> list[str]:
    parts, stale_here = read_store_contributions(path, exclude_tags)
    for part in parts:
        if isinstance(part, ModelEdges):
            fields.setdefault(part.model_name, part.projected_fields)
    _merge((qualify(p, name) for p in parts), nodes, edges, _source(path))
    return [f"{name}:{export_id}" if name else export_id for export_id in stale_here]


def _merge(parts: Iterable[EdgeContribution], nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], source: dict) -> None:
    for part in parts:
        edges += part.edges
        for node in part.nodes:
            nodes.setdefault(node.id, _stamped(node, source))


def _stamped(node: EdgeNodeRecord, source: dict) -> EdgeNodeRecord:
    return node.model_copy(update={"facets": {**node.facets, "source": source}})


def _source(store_path: Path) -> dict:
    return {"generated_from": "sldb.store.edge_index", "store_path": str(store_path), "hash_a": load_store_index(store_path).hash_a}
