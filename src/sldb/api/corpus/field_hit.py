"""A ranked field: which field of which document matched, its score, and the text that did.

`text` is the field's own, not the document's: a caller showing why something ranked has
the matching passage without re-reading the document.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sldb.api.corpus.field_entry import FieldEntry


@dataclass(frozen=True)
class FieldHit:
    """A ranked field of a document. `payload` is the whole document as sldb extracted it."""

    id: str
    document_id: str
    field: str
    model: str
    name: str
    score: float
    text: str
    payload: dict[str, Any]
    tags: tuple[str, ...] = ()

    _FROM_ENTRY = ("id", "document_id", "field", "model", "name", "text", "payload", "tags")

    @classmethod
    def of(cls, entry: "FieldEntry", score: float) -> "FieldHit":
        carried = {name: getattr(entry, name) for name in cls._FROM_ENTRY}
        return cls(score=round(score, 4), **carried)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
