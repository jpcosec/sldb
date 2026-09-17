"""One store's shards read back as contributions: the store's, each model's, each document's
— a document carrying an excluded tag leaves only its tag nodes behind — plus which tracked
documents have no current shard."""

from __future__ import annotations

from pathlib import Path

from sldb.store import documents_hash
from sldb.store.io import load_store_index
from sldb.store.io.shard_compose import compose_edges_documents
from sldb.store.io.shards import load_edges_shard
from sldb.store.layout import edges_model_shard_path, edges_store_shard_path
from sldb.store.models import DocEdges, EdgeContribution, ModelEdges


def read_store_contributions(store_path: Path, exclude_tags: frozenset[str]) -> tuple[list[EdgeContribution], list[str]]:
    """(contributions in a stable order, export ids of the documents whose shard is stale)."""
    parts: list[EdgeContribution] = [p for p in [load_edges_shard(edges_store_shard_path(store_path), EdgeContribution)] if p]
    stale: list[str] = []
    for m in sorted(load_store_index(store_path).models, key=lambda m: m.name):
        parts += [p for p in [load_edges_shard(edges_model_shard_path(store_path, m.name), ModelEdges)] if p]
        shards = compose_edges_documents(store_path, m.name)
        parts += [_filtered(shard, exclude_tags) for shard in shards]
        stale += _stale_documents(store_path, m.name, {s.doc_name: (s.hash_c, s.hash_d) for s in shards})
    return parts, stale


def _filtered(shard: DocEdges, exclude_tags: frozenset[str]) -> EdgeContribution:
    """The index holds everything; leaving a tag out (pron's ledger) is the reader's choice."""
    if not exclude_tags.intersection(shard.semantic_tags):
        return shard
    return EdgeContribution(nodes=[n for n in shard.nodes if n.node_type == "semantic_tag"])


def _stale_documents(store_path: Path, model_name: str, shard_hashes: dict[str, tuple[str, str]]) -> list[str]:
    from sldb.store.layout import project_root

    root = project_root(store_path)
    entries = documents_hash.entries_of(store_path, model_name)
    moved = [e for e in entries if shard_hashes.get(e.name) != (e.hash_c, e.hash_d)]
    return [f"{model_name}:{e.name}" for e in moved if e.name in shard_hashes or (root / e.path).exists()]
