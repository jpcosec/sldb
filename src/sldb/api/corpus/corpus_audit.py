"""Auditing a corpus's index against its store: documents never indexed (`missing`),
indexed from other content (`stale`), indexed and no longer in the corpus (`orphan`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sldb.api.corpus.corpus import Corpus


class CorpusAudit:
    """One audit of one corpus, of its documents or of its fields.

    The three drift lists mean the same either way; only the unit changes, so `per_field`
    picks which entries and which index are compared rather than duplicating the audit.
    """

    def __init__(self, corpus: "Corpus", per_field: bool = False) -> None:
        self.corpus = corpus
        self.per_field = per_field

    def __call__(self) -> dict[str, Any]:
        source = self.corpus.field_entries if self.per_field else self.corpus.entries
        index = self.corpus.field_index if self.per_field else self.corpus.index
        entries = {e.id: e for e in source()}
        indexed = index.entries_by_hash()
        missing = sorted(k for k in entries if k not in indexed)
        stale = sorted(k for k, e in entries.items() if k in indexed and indexed[k] != e.hash)
        orphan = sorted(k for k in indexed if k not in entries)
        return self._report(entries, indexed, missing, stale, orphan)

    def _report(self, entries, indexed, missing, stale, orphan) -> dict[str, Any]:
        """The audit summary, with the counts and the three drift lists."""
        drift = {"missing": missing, "stale": stale, "orphan": orphan}
        return {
            **self._unit_header(),
            "corpus": len(entries),
            "indexed": len(indexed),
            **drift,
            "clean": not (missing or stale or orphan),
        }

    def _unit_header(self) -> dict[str, Any]:
        """What produced this index: the embedder, the unit indexed and the text mapping."""
        projection = self.corpus.field_projection if self.per_field else self.corpus.projection
        unit = "field" if self.per_field else "document"
        return {"embedder": self.corpus.matcher.id(), "unit": unit, "text": projection.text_id}
