"""The write journal of the substrate: one file per applied batch under `.sldb/core/write_journal/`,
with what is needed to revert it (docs/architecture/journal-authority.md, "The write journal").

Each entry keeps the batch id, its order in the store, the actor and time, and per document the
before-image (model, path, payload; null when the batch created it) and the content hash it left
(`after_hash`; null when the batch removed it), plus `inverse`, the batch that undoes it, guarded by
those hashes. An undone batch is marked `reverted_at`. The journal is not part of the store hash
(`store_index` hashes documents only). Callers hold the store lock."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sldb.store.layout import core_dir


def journal_dir(store_path: Path) -> Path:
    return core_dir(store_path) / "write_journal"


def entries(store_path: Path) -> list[dict[str, Any]]:
    """Every entry, oldest first (by `order`)."""
    directory = journal_dir(store_path)
    if not directory.is_dir():
        return []
    found = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(directory.glob("*.json"))]
    return sorted(found, key=lambda e: e["order"])


def record(store_path: Path, actor: str, documents: list[dict[str, Any]], inverse: list[dict[str, Any]]) -> dict[str, Any]:
    """Append the entry of a batch just applied."""
    existing = entries(store_path)
    order = (existing[-1]["order"] + 1) if existing else 1
    entry = {"batch_id": uuid.uuid4().hex[:12], "order": order, "actor": actor, "at": _now(), "documents": documents, "inverse": inverse, "reverted_at": None}
    _write(store_path, entry)
    return entry


def mark_reverted(store_path: Path, batch_ids: list[str]) -> None:
    for entry in entries(store_path):
        if entry["batch_id"] in batch_ids:
            _write(store_path, {**entry, "reverted_at": _now()})


def unreverted(store_path: Path) -> list[dict[str, Any]]:
    """Entries not yet undone, oldest first."""
    return [e for e in entries(store_path) if not e["reverted_at"]]


def _write(store_path: Path, entry: dict[str, Any]) -> None:
    directory = journal_dir(store_path)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{entry['order']:08d}-{entry['batch_id']}.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(entry, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(target)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
