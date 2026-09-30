"""What the HTTP corpus reads of a document: every string field, not only `summary`.

`IndexProjection`'s default text is the `summary` field, which leaves out every model that has
none (most of them), so the server declares its own projection instead of ranking nothing.
"""

from __future__ import annotations

from typing import Any

from sldb.api.corpus.index_projection import IndexProjection


def all_strings(payload: dict[str, Any]) -> str:
    """The non-empty string values of the payload, one per line, in field order."""
    values = (value.strip() for value in payload.values() if isinstance(value, str))
    return "\n".join(value for value in values if value)


HTTP_PROJECTION = IndexProjection(text=all_strings, text_id="text")
