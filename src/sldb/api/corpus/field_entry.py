"""One indexed field of one document: `Model:doc#field`.

Carries the document it belongs to, so a hit on a field can be read as a hit on its
document without a second lookup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FieldEntry:
    """One field of one document of the corpus, identified as `Model:doc#field`."""

    id: str
    document_id: str
    field: str
    model: str
    name: str
    store: str | None
    text: str
    hash: str
    payload: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = ()
