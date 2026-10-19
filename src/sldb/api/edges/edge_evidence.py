"""Edges with their evidence: the target's hash, the source's contract, and who derived them.

Opt-in (`stamp_evidence`, `sldb edges show --evidence`): the evidence is computed on read from
the store indexes, so the shards stay keyed by their own document and nothing else moves.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.edge_evidence import stamp
from sldb.store.edge_index.federation import federated_stores, qualify_id
from sldb.store.edge_index.node_ids import doc_node_id, model_node_id
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.models import EdgeRecord


def stamp_evidence(store: str | Path | None, edges: list[EdgeRecord], include_linked: bool = True) -> list[EdgeRecord]:
    """`edges` with `metadata.evidence` (see `sldb.store.edge_index.edge_evidence`)."""
    store_path = open_store(store, mode="readonly").store_path
    hashes: dict[str, str] = {}
    contracts: dict[str, str] = {}
    for path, name in federated_stores(store_path, include_linked):
        _collect(path, name, hashes, contracts)
    return stamp(edges, hashes, contracts, {"name": "sldb", "version": _version()})


def _collect(store_path: Path, link: str | None, hashes: dict[str, str], contracts: dict[str, str]) -> None:
    root = project_root(store_path)
    for model in load_store_index(store_path).models:
        index = load_models_index(root / model.models_index)
        hashes[qualify_id(model_node_id(model.name), link)] = index.model_hash
        contracts.setdefault(model.name, index.contract_hash)
        for doc in load_documents_index(root / index.documents_index).documents:
            hashes[qualify_id(doc_node_id(f"{model.name}:{doc.name}"), link)] = doc.content_hash


def _version() -> str:
    try:
        return version("structuredLanguageDB")
    except PackageNotFoundError:
        return "unknown"
