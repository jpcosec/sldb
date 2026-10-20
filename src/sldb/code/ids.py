"""Unique fact ids across one scan: a repeated candidate gets `~2`, `~3`... in scan order."""

from __future__ import annotations


class Ids:
    def __init__(self) -> None:
        self.seen: dict[str, int] = {}

    def take(self, candidate: str) -> str:
        n = self.seen[candidate] = self.seen.get(candidate, 0) + 1
        return candidate if n == 1 else f"{candidate}~{n}"
