"""The hash of what a document says, apart from who signed it and when: its text without the
`sldb` provenance block. Equal content hashes mean the same content however many times it was
re-stamped (`sldb.by/at/via` and the hashes derived from them differ on every write)."""

from __future__ import annotations

import hashlib
from typing import Any

from sldb.api.stores.store_location import StoreLocation
from sldb.models.provenance_block import strip_block
from sldb.store.source_guard import read_source_bytes


def document_content_hash(location: StoreLocation, doc: Any) -> str:
    """`sha256:<hex>` of the text of the tracked document `doc` with its provenance block stripped."""
    text = read_source_bytes(location.project_root / doc.path).decode("utf-8")
    return "sha256:" + hashlib.sha256(strip_block(text).encode("utf-8")).hexdigest()
