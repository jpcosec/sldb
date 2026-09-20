"""The indexed corpus of a store: which documents a consumer can retrieve by similarity,
kept fresh against the store. A runtime that retrieves by meaning declares its policy
once as an `IndexProjection`; the index, the refresh and the audit are general and live
here.

Identity is always the export id (`Model:doc`, `store:Model:doc`), never the bare name.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from sldb.api.corpus.corpus_audit import CorpusAudit
from sldb.api.corpus.corpus_entries import corpus_entries, select_hits
from sldb.api.corpus.hit import Hit
from sldb.api.corpus.index_projection import IndexProjection
from sldb.api.matching.document_index import DocumentIndex
from sldb.api.matching.matcher import Matcher


class Corpus:
    """The documents of a store that can be retrieved by similarity, and their index."""

    def __init__(
        self,
        store: str | Path,
        pythonpath: str | None,
        derived_dir: Path,
        projection: IndexProjection | None = None,
        embedder: Any | None = None,
        matcher: Matcher | None = None,
    ) -> None:
        self.store = Path(store)
        self.pythonpath = pythonpath
        self.derived_dir = derived_dir
        self.projection = projection or IndexProjection()
        self.matcher = matcher or Matcher(embedder)
        self._index: DocumentIndex | None = None

    @property
    def index_path(self) -> Path:
        safe = self.matcher.id().replace("/", "_").replace(":", "_")
        name = f"docs.{safe}.json" if self.projection.text_id == "summary" else f"docs.{self.projection.text_id}.{safe}.json"
        return self.derived_dir / name

    @property
    def index(self) -> DocumentIndex:
        if self._index is None:
            self._index = DocumentIndex(self.matcher, self.index_path)
        return self._index

    def entries(self):
        return corpus_entries(self)

    def refresh(self) -> dict[str, int]:
        return self.index.index((e.id, e.hash, e.text) for e in self.entries())

    def refresh_if_stale(self) -> dict[str, int] | None:
        report = self.audit()
        if report["missing"] or report["stale"] or report["orphan"]:
            return self.refresh()
        return None

    def audit(self) -> dict[str, Any]:
        return CorpusAudit(self)()

    def rank(
        self,
        query: str,
        k: int | None = None,
        threshold: float = 0.0,
        among: Sequence[str] | None = None,
        refresh: bool = True,
    ) -> list[Hit]:
        if refresh:
            self.refresh_if_stale()
        by_id = {e.id: e for e in self.entries()}
        allowed = set(among) if among is not None else None
        ranked = self.index.rank(query, k=None, threshold=threshold)
        return select_hits(ranked, by_id, allowed, k)

    def vectors(self) -> dict[str, list[float]]:
        return self.index.vectors()
