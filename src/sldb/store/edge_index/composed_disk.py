"""The composed edge index kept on disk between processes (H11): `<cache>/composed/<request>.json`
in the calling store's `.sldb_cache`. A new process that finds the shards where the file saw
them reads it (plain JSON, never executed) instead of parsing every shard again. The file
holds the key it was composed under; any difference in it is a miss, so a changed store, a
changed linked store, a moved model contract or another sldb version reads the shards as before."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from sldb.store.edge_index.cache_keys import edge_shard_version
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.live_stale import ModelTypeOf
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io import load_store_index
from sldb.store.layout import cache_dir, core_dir, project_root

FORMAT = "1"


def disk_key(stores: list[tuple[Path, str | None]], include_linked: bool, exclude_tags: frozenset[str], model_type_of: ModelTypeOf | None) -> dict[str, Any]:
    """What a composed index depends on: every federated store's shard and document-shard
    state (the signature `compose_edge_index` already keeps in memory, without this process's
    rebuild counter) and, for the derived anchor states, the models' contracts."""
    key = {
        "format": FORMAT, "edges": edge_shard_version(), "linked": include_linked, "tags": sorted(exclude_tags),
        "stores": [[str(p), n, list(shards_signature(p)[1:]), _documents_state(p)] for p, n in stores],
        "contracts": None if model_type_of is None else [_stamp(p, model_type_of) for p, _ in stores],
    }
    return json.loads(json.dumps(key))  # as a file reads it back: lists, not tuples


def load_composed(calling: Path, key: dict[str, Any]) -> tuple[EdgeIndex, list] | None:
    """(index, facts) saved under exactly this key; None on a miss or an unreadable file."""
    try:
        saved = json.loads(_file(calling, key).read_text(encoding="utf-8"))
        return (EdgeIndex.model_validate(saved["index"]), saved["facts"]) if saved["key"] == key else None
    except (OSError, ValueError, KeyError, TypeError):
        return None


def save_composed(calling: Path, key: dict[str, Any], index: EdgeIndex, facts: list) -> None:
    """Keep the composed index for the next process; a store that cannot be written is not an error."""
    path = _file(calling, key)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps({"key": key, "index": index.model_dump(mode="json"), "facts": facts}), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        tmp.unlink(missing_ok=True)


def _file(calling: Path, key: dict[str, Any]) -> Path:
    request = json.dumps([key["linked"], key["tags"], key["contracts"] is None, key["format"]])
    return cache_dir(calling) / "composed" / f"{hashlib.sha256(request.encode()).hexdigest()[:16]}.json"


def _documents_state(store_path: Path) -> list:
    """Where the tracked paths come from: the mtime of each model's document-shard directory."""
    try:
        with os.scandir(core_dir(store_path) / "documents") as found:
            return sorted([e.name, e.stat().st_mtime_ns] for e in found)
    except OSError:
        return []


def _stamp(store_path: Path, model_type_of: ModelTypeOf) -> list[str]:
    """Per registered model, what the anchor states read of its class."""
    from sldb.store.model_contract import contract_signature

    root = project_root(store_path)
    classes = [model_type_of(m.model_ref, root) for m in load_store_index(store_path).models]
    return [f"{contract_signature(c)}|{getattr(c, '__doc_anchors__', None)!r}|{getattr(c, '__contract__', None)!r}" for c in classes]
