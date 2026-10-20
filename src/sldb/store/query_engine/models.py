from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RuntimeDocument:
    """
    In-memory representation of a tracked document and its payload.
    """

    store_name: str
    store_path: Path
    model_name: str
    model_type: type
    name: str
    path: str
    payload: dict[str, Any]
    semantic_tags: list[str]
    source_hash: str = ''
    content_hash: str = ''
    # Per-field `content_hash`, as the document's shard recorded it. Empty means "not computed"
    # (a store written before `field_hashes`, or a document that no longer extracts), never
    # "no fields": a per-field consumer with nothing to compare against indexes the whole
    # document instead of concluding nothing moved.
    field_hashes: dict[str, str] = field(default_factory=dict)
    # The `sldb` block as indexed; None when the document carries none (docs/architecture/provenance.md).
    provenance: dict[str, Any] | None = None
