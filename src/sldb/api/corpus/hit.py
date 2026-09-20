"""A ranked document of the corpus: its export id, its score, and the payload as sldb
extracted it. Indexable by key too, for a consumer that expects rows.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sldb.api.corpus.corpus_entry import CorpusEntry


@dataclass(frozen=True)
class Hit:
    """A ranked document. `payload` is the document as sldb extracted it."""

    id: str
    model: str
    name: str
    score: float
    payload: dict[str, Any]
    tags: tuple[str, ...] = ()

    @classmethod
    def of(cls, entry: "CorpusEntry", score: float) -> "Hit":
        return cls(
            id=entry.id,
            model=entry.model,
            name=entry.name,
            score=round(score, 4),
            payload=entry.payload,
            tags=entry.tags,
        )

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
