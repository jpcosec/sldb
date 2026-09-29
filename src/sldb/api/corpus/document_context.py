"""What every field of one document shares while its entries are built.

Holding it once keeps building one entry a two-liner, and keeps the document's identity
(its export id and its per-field hashes) resolved a single time per document instead of
once per field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sldb.api.corpus.field_entry import FieldEntry
from sldb.api.corpus.field_projection import field_id


@dataclass(frozen=True)
class DocumentContext:
    """What every field of one document shares, so building one entry stays a two-liner."""

    record: Any
    model: str
    store: str | None
    document_id: str
    hashes: dict[str, str]

    def entry(self, name: str, text: str) -> FieldEntry:
        return FieldEntry(
            id=field_id(self.document_id, name), document_id=self.document_id, field=name,
            model=self.model, name=self.record.name, store=self.store, text=text,
            hash=self.hashes.get(name, ""), payload=self.record.payload or {},
            tags=tuple(self.record.semantic_tags or ()),
        )
