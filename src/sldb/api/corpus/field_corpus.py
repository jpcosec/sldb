"""The per-field half of a corpus: indexing, auditing and ranking fields instead of documents.

Split from `Corpus` so each file keeps one subject. A field index is the same machinery with a
finer key (`Model:doc#field`) and a finer hash (the field's own), which is what makes a re-index
embed only the fields that moved.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from sldb.api.corpus.corpus_audit import CorpusAudit
from sldb.api.corpus.field_entries import field_entries, select_field_hits
from sldb.api.corpus.field_hit import FieldHit
from sldb.api.matching.document_index import DocumentIndex


class FieldCorpusMixin:
    """The per-field surface of a corpus. Mixed into `Corpus`, never used on its own."""

    @property
    def field_index_path(self) -> Path:
        """The per-field index's own derived file, never shared with the document index."""
        safe = self.matcher.id().replace("/", "_").replace(":", "_")
        return self.derived_dir / f"fields.{self.field_projection.text_id}.{safe}.json"

    @property
    def index(self) -> DocumentIndex:
        if self._index is None:
            self._index = DocumentIndex(self.matcher, self.index_path)
        return self._index

    @property
    def field_index(self) -> DocumentIndex:
        """The same index, keyed by `Model:doc#field` instead of by document."""
        if self._field_index is None:
            self._field_index = DocumentIndex(self.matcher, self.field_index_path)
        return self._field_index

    def field_entries(self):
        return field_entries(self)

    def refresh_fields(self) -> dict[str, int]:
        """Embed the fields whose own hash moved; reuse the rest."""
        return self.field_index.index((e.id, e.hash, e.text) for e in self.field_entries())

    def rank_fields(
        self,
        query: str,
        k: int | None = None,
        threshold: float = 0.0,
        among: Sequence[str] | None = None,
        refresh: bool = True,
    ) -> list[FieldHit]:
        """The fields closest to `query`, best first.

        `among` filters by field id (`Model:doc#field`) or by document id: naming a document
        admits every one of its fields, which is what a caller narrowing to a document means.
        """
        if refresh:
            self.refresh_fields_if_stale()
        by_id = {e.id: e for e in self.field_entries()}
        allowed = set(among) if among is not None else None
        ranked = self.field_index.rank(query, k=None, threshold=threshold)
        return select_field_hits(ranked, by_id, allowed, k)

    def refresh_fields_if_stale(self) -> dict[str, int] | None:
        report = self.audit_fields()
        if report["missing"] or report["stale"] or report["orphan"]:
            return self.refresh_fields()
        return None

    def audit_fields(self) -> dict[str, Any]:
        return CorpusAudit(self, per_field=True)()

    def field_vectors(self) -> dict[str, list[float]]:
        return self.field_index.vectors()
