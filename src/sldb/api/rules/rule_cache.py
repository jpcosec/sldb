"""The derived cache of the rules (GO08, rules.md §9): `<.sldb_cache>/rules/` of the store.

One JSON file per rule, named by the rule's `content_hash`: `results` maps each document of the
rule's family to its finding (`Finding.as_dict()`, or null when the rule holds or does not
apply) and `stamps` to what that result was computed from (`dirty_set.stamps_of`). An absent,
unreadable or other-version file is an absent cache: everything recomputes. The cache is never
authority and nothing outside it is written; a file that cannot be written is left alone.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from sldb.store.io.shards import load_document_shard
from sldb.store.layout import cache_dir, documents_shard_path

VERSION = 1
DIRTY = "dirty"


def rules_dir(store_path: Path) -> Path:
    return cache_dir(store_path) / "rules"


def read_json(path: Path) -> dict[str, Any] | None:
    """The file's object, or None when it is absent, unreadable or of another version."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("version") == VERSION else None


def write_json(path: Path, data: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"version": VERSION, **data}, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    except OSError:
        return


def read_results(store_path: Path, key: str) -> tuple[dict[str, Any], dict[str, str]]:
    """`(results, stamps)` of the rule whose content hash is `key`; empty maps when absent."""
    data = read_json(rules_dir(store_path) / f"{key}.json") or {}
    results, stamps = data.get("results"), data.get("stamps")
    return (results, stamps) if isinstance(results, dict) and isinstance(stamps, dict) else ({}, {})


def write_results(store_path: Path, key: str, results: dict[str, Any], stamps: dict[str, str]) -> None:
    write_json(rules_dir(store_path) / f"{key}.json", {"results": results, "stamps": stamps})


def prune(store_path: Path, keep: set[str]) -> None:
    """Drop the files of rules that no longer exist (an edited rule leaves its old hash)."""
    for path in rules_dir(store_path).glob("*.json"):
        if path.stem not in keep | {DIRTY}:
            path.unlink(missing_ok=True)


def rule_hash(store_path: Path, rule: dict[str, Any]) -> str:
    """The rule document's `content_hash` (GO06), else a hash of the payload it was read with."""
    model, _, name = rule["id"].partition(":")
    entry = load_document_shard(documents_shard_path(store_path, model, name))
    if entry is not None and entry.content_hash:
        return entry.content_hash
    return hashlib.sha256(json.dumps(rule, sort_keys=True, default=str).encode()).hexdigest()
