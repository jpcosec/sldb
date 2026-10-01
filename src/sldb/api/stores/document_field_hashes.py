"""Extract a document once and sign both its payload and each field of it.

Split out of `index_refresh` (which composes them into a refresh) so each file stays small;
`index_refresh` re-exports the names its compat importers expect.
"""

from __future__ import annotations

from typing import Any

from sldb.store.hashing import hash_field_map_of, hash_payload


def _extracted_payload(mtype: Any, doc: Any, text: str, force: bool) -> Any:
    """The document's payload, from the runtime cache when it can be trusted.

    The cached payload is skipped when the contract moved: it was extracted under the previous
    contract, which is exactly what must not win here.
    """
    from sldb.store.runtime_cache import payload_of
    from sldb.store.codec import default_codec
    payload = None if force else payload_of(doc.path, doc.source_hash, mtype)
    return payload if payload is not None else default_codec.extract(mtype, text)


def _field_hashes(mtype: Any, m_name: str, doc: Any, text: str, force: bool = False) -> tuple[str, dict[str, str]]:
    """The document's `content_hash` and its per-field map, from one extraction.

    Both are empty when the Markdown no longer extracts (reported by `stores check`): an empty
    map means "unknown", so a consumer comparing against it falls back to the whole document
    rather than concluding no field moved.
    """
    try:
        payload = _extracted_payload(mtype, doc, text, force)
        field_map = hash_field_map_of(payload) if isinstance(payload, dict) else {}
        return hash_payload(payload), field_map
    except Exception:
        return "", {}


def _field_hash(mtype: Any, m_name: str, doc: Any, text: str, force: bool = False) -> str:
    """`_field_hashes` without the per-field map. Kept for callers that only want `content_hash`."""
    return _field_hashes(mtype, m_name, doc, text, force)[0]
