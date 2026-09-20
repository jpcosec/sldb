"""Documents of a store ranked by similarity to a query. The vectors live in one derived
file outside git, keyed by the document's content hash, so a re-index embeds only what
changed. With a Matcher that has no Embedder there are no vectors: the texts are kept and
ranked with difflib, and the file says which it is.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.matching.document_persist import read_index, write_index
from sldb.api.matching.matcher import Matcher, cosine


class DocumentIndex:
    """Documents of a store ranked by similarity to a query."""

    def __init__(self, matcher: Matcher, cache_path: Path):
        self.matcher = matcher
        self.cache_path = Path(cache_path)
        self._entries: dict[str, dict] = read_index(self.cache_path, self.embedder_id)

    @property
    def embedder_id(self) -> str:
        return self.matcher.id()

    def index(self, items: Iterable[tuple[str, str, str]]) -> dict[str, int]:
        keep, todo, reused = self._partition(items)
        keep.update(self._embedded(todo))
        dropped = len(set(self._entries) - set(keep))
        self._entries = keep
        write_index(self.cache_path, self.embedder_id, self._entries)
        return {"embedded": len(todo), "reused": reused, "dropped": dropped}

    def _partition(
        self, items: Iterable[tuple[str, str, str]]
    ) -> tuple[dict[str, dict], list[tuple[str, str, str]], int]:
        keep: dict[str, dict] = {}
        todo: list[tuple[str, str, str]] = []
        reused = 0
        for key, h, text in list(items):
            if self._unchanged(key, h):
                keep[key] = self._entries[key]
                reused += 1
            else:
                todo.append((key, h, text))
        return keep, todo, reused

    def _unchanged(self, key: str, h: str) -> bool:
        prev = self._entries.get(key)
        return prev is not None and prev.get("hash") == h

    def _embedded(self, todo: list[tuple[str, str, str]]) -> dict[str, dict]:
        if self.matcher.embedder is None:
            return {key: {"hash": h, "text": text} for key, h, text in todo}
        if not todo:
            return {}
        vectors = self.matcher.embedder.embed([t for _, _, t in todo])
        return {
            key: {"hash": h, "vector": [float(x) for x in v]}
            for (key, h, _), v in zip(todo, vectors)
        }

    def keys(self) -> list[str]:
        return sorted(self._entries)

    def entries_by_hash(self) -> dict[str, str]:
        return {k: e.get("hash", "") for k, e in self._entries.items()}

    def vectors(self) -> dict[str, list[float]]:
        return {k: list(e["vector"]) for k, e in self._entries.items() if "vector" in e}

    def rank(
        self, query: str, k: int | None = None, threshold: float = 0.0
    ) -> list[tuple[str, float]]:
        if not self._entries:
            return []
        scored = self._scored(query)
        out = sorted(
            ((key, s) for key, s in scored if s >= threshold),
            key=lambda kv: (-kv[1], kv[0]),
        )
        return out[:k] if k is not None else out

    def _scored(self, query: str) -> list[tuple[str, float]]:
        if self.matcher.embedder is None:
            return self._text_scored(query)
        return self._vector_scored(query)

    def _text_scored(self, query: str) -> list[tuple[str, float]]:
        return [
            (key, self.matcher.fallback.similarity(query, e.get("text", "")))
            for key, e in self._entries.items()
        ]

    def _vector_scored(self, query: str) -> list[tuple[str, float]]:
        q = self.matcher.embedder.embed([query])[0]
        return [
            (key, cosine(q, e["vector"]))
            for key, e in self._entries.items()
            if "vector" in e
        ]
