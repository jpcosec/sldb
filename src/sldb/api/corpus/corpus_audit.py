"""Auditing a corpus's index against its store: documents never indexed (`missing`),
indexed from other content (`stale`), indexed and no longer in the corpus (`orphan`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sldb.api.corpus.corpus import Corpus


class CorpusAudit:
    """One audit of one corpus."""

    def __init__(self, corpus: "Corpus") -> None:
        self.corpus = corpus

    def __call__(self) -> dict[str, Any]:
        entries = {e.id: e for e in self.corpus.entries()}
        indexed = self.corpus.index.entries_by_hash()
        missing = sorted(k for k in entries if k not in indexed)
        stale = sorted(k for k, e in entries.items() if k in indexed and indexed[k] != e.hash)
        orphan = sorted(k for k in indexed if k not in entries)
        return self._report(entries, indexed, missing, stale, orphan)

    def _report(self, entries, indexed, missing, stale, orphan) -> dict[str, Any]:
        """The audit summary, with the counts and the three drift lists."""
        return {
            "embedder": self.corpus.matcher.id(),
            "text": self.corpus.projection.text_id,
            "corpus": len(entries),
            "indexed": len(indexed),
            "missing": missing,
            "stale": stale,
            "orphan": orphan,
            "clean": not (missing or stale or orphan),
        }
