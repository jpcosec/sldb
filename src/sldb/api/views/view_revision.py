"""The revision of a view's result (GD25, q16): what changes when anything it read changes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from sldb.api.views.view_source import view_store
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path


def revision(store_path: Path, index: Any, row_ids: set[str], view: Any, rule_ids: list[str]) -> str:
    """sha256 of the rows' documents' `source_hash` (sorted), the ViewDoc's and the used
    RuleDocs' `content_hash`, and the store's shards signature (an edge reaching a row from
    a new document moves the shards, not the row). `view` is the ViewDoc's index node: its
    hash is read from the store that tracks it, a linked one included (H9)."""
    read = {
        "documents": sorted(source_hash(index, export_id) for export_id in row_ids),
        "view": content_hash(view_store(view), view.semantics["export_id"]),
        "rules": [content_hash(store_path, rule_id) for rule_id in sorted(set(rule_ids))],
        "shards": shards_signature(store_path),
    }
    return hashlib.sha256(json.dumps(read, sort_keys=True, default=list).encode("utf-8")).hexdigest()


def source_hash(index: Any, export_id: str) -> str:
    node = index.node(export_id)
    return node.source_hash if node is not None else ""


def content_hash(store_path: Path, export_id: str) -> str:
    """A local document's `content_hash` from its shard; empty when the shard is missing."""
    model, name = export_id.split(":")[-2], export_id.split(":")[-1]
    entry = load_document_shard(documents_shard_path(store_path, model, name))
    return entry.content_hash if entry is not None else ""
