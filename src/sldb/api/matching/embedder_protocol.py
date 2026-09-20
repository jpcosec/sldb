"""The approximate-matching port: an application injects an Embedder; without one the
matcher falls back to difflib. It never executes anything, it only ranks neighbors to offer.
"""

from __future__ import annotations

from typing import Protocol, Sequence


class Embedder(Protocol):
    def id(self) -> str: ...
    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...
