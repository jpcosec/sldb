"""Ranking candidates for a query: with an Embedder when the application gave one, difflib
otherwise. `cosine` is the similarity over two vectors.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Sequence

from sldb.api.matching.difflib_matcher import DifflibMatcher
from sldb.api.matching.embedder_protocol import Embedder


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class Matcher:
    """Ranks candidates for a query with an Embedder when given, difflib otherwise."""

    def __init__(
        self, embedder: Embedder | None = None, cache_path: Path | None = None
    ):
        self.embedder = embedder
        self.fallback = DifflibMatcher()
        self._cache: dict[str, list[float]] = {}
        self.cache_path: Path | None = None
        self.bind_cache(cache_path)

    def bind_cache(self, path: Path | None) -> None:
        """Keep the vectors in a derived file. Only with an Embedder; difflib has nothing to cache."""
        self.cache_path = path if self.embedder is not None else None
        self._cache = {}
        if self.cache_path is not None and self.cache_path.exists():
            try:
                self._cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self._cache = {}

    def id(self) -> str:
        return self.embedder.id() if self.embedder else self.fallback.id()

    def rank(
        self,
        query: str,
        candidates: Sequence[tuple[str, str]],
        k: int = 3,
        threshold: float = 0.0,
    ) -> list[tuple[str, float]]:
        """candidates are (key, text). Returns [(key, score)] best first, above threshold."""
        scored = self._scored(query, candidates)
        best: dict[str, float] = {}
        for key, score in scored:
            if score >= threshold and score > best.get(key, -1):
                best[key] = score
        return sorted(best.items(), key=lambda kv: -kv[1])[:k]

    def _scored(
        self, query: str, candidates: Sequence[tuple[str, str]]
    ) -> list[tuple[str, float]]:
        if self.embedder is None:
            return [
                (key, self.fallback.similarity(query, text)) for key, text in candidates
            ]
        vectors = self._embed([query, *[t for _, t in candidates]])
        return [
            (key, max(cosine(vectors[0], v), self.fallback.similarity(query, text)))
            for (key, text), v in zip(candidates, vectors[1:])
        ]

    def _embed(self, texts: list[str]) -> list[list[float]]:
        assert self.embedder is not None
        missing = [t for t in texts if t not in self._cache]
        if missing:
            for t, v in zip(missing, self.embedder.embed(missing)):
                self._cache[t] = v
            self._write_cache()
        return [self._cache[t] for t in texts]

    def _write_cache(self) -> None:
        """Persist the vectors, best effort: a missing cache file never breaks ranking."""
        if self.cache_path is None:
            return
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps(self._cache), encoding="utf-8")
        except OSError:
            pass
