"""A document signed under another field set: its per-field hashes name a field the model no
longer has.

The model's contract hash cannot see this for one document: any write of another document of
the same model re-stamps the contract to the current class, and from then on the model reads
as unmoved while this document's hashes still come from the old fields. The key set of its
`field_hashes` is the document's own record of the contract it was signed under.
"""

from __future__ import annotations

from typing import Any


def signed_under_other_fields(field_hashes: dict[str, str] | None, model_type: Any) -> bool:
    """True when the stored field map names a field `model_type` does not declare.

    Only that direction is evidence: extraction leaves out fields that are empty or absent from
    the text, so a declared field missing from the map proves nothing.
    """
    if model_type is None or not field_hashes:
        return False
    return bool(set(field_hashes) - set(getattr(model_type, "model_fields", {})))
