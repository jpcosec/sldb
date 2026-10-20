"""What one committed version of a document says: its provenance block, its hashes, its fields."""

from __future__ import annotations

from typing import Any

from sldb.api.documents.provenance_stamp import provenance_of
from sldb.store.hashing import hash_fields_with_map, hash_text


def version_facts(model_type: type, text: str) -> dict[str, Any]:
    """`{provenance, source_hash, content_hash, field_hashes}` of `text` under `model_type`;
    a version that does not extract has an empty content hash and no field map."""
    found = provenance_of(text)
    try:
        content_hash, field_hashes = hash_fields_with_map(model_type, text)
    except Exception:  # noqa: BLE001 - an older version may predate the model's contract
        content_hash, field_hashes = "", {}
    provenance = {**found.model_dump(by_alias=True), "declared": found.declared}
    return {"provenance": provenance, "source_hash": hash_text(text), "content_hash": content_hash, "field_hashes": field_hashes}


def changed_fields(now: dict[str, str], before: dict[str, str]) -> list[str]:
    """The fields whose hash differs between two versions (added and dropped ones included)."""
    return sorted(name for name in set(now) | set(before) if now.get(name) != before.get(name))
