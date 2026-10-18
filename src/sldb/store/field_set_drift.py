"""A document signed under another field set: its per-field hashes name a field the model no
longer has.

The model's contract hash cannot see this for one document: any write of another document of
the same model re-stamps the contract to the current class, and from then on the model reads
as unmoved while this document's hashes still come from the old fields. The key set of its
`field_hashes` is the document's own record of the contract it was signed under.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.store.hashing import hash_fields_with_map


def signed_under_other_fields(field_hashes: dict[str, str] | None, model_type: Any, current: Iterable[str] | None = None) -> bool:
    """True when the stored field map names a field `model_type` does not declare.

    Only that direction is evidence: extraction leaves out fields that are empty or absent from
    the text, so a declared field missing from the map proves nothing.

    `current` is the key set today's extraction of the same document yields. A model with
    `extra="allow"` promotes undeclared frontmatter keys into the payload, so an undeclared key
    is not a sign of another contract when the current class still produces it; without
    `current` the check stays conservative (a caller about to re-extract anyway loses nothing).
    """
    if model_type is None or not field_hashes:
        return False
    stale = set(field_hashes) - set(getattr(model_type, "model_fields", {}))
    return bool(stale - set(current or ()))


def document_drifted(doc: Any, root: Path, model_type: Any) -> bool:
    """Whether a tracked document was signed under another field set. Only a document whose map
    names an undeclared field is re-extracted, to tell an `extra="allow"` key it still yields
    from one the current class no longer produces."""
    if not signed_under_other_fields(doc.field_hashes, model_type):
        return False
    path = root / doc.path
    if not path.exists():
        return True
    return signed_under_other_fields(doc.field_hashes, model_type, hash_fields_with_map(model_type, path.read_text(encoding="utf-8"))[1])
