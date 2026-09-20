"""Hash an entry's fields into its chaining digest (SHA-256)."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def hash_entry_fields(fields: dict[str, Any]) -> str:
    """The SHA-256 of an entry's fields, everything except `entry_hash` itself."""
    text = json.dumps(fields, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
