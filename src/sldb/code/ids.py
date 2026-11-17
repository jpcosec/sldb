"""Unique fact ids across one scan: a repeated candidate gets `~2`, `~3`... in scan order.

Two passes: `take` gives an id now (module, class, function, method and the TS and SQL kinds);
`take_late` queues a fact (`assignment`, `call`) whose id `flush` gives after every `take` of
the scan, so a late fact never takes the id a definition or module of another file would have.
"""

from __future__ import annotations

from typing import Any


class Ids:
    def __init__(self) -> None:
        self.seen: dict[str, int] = {}
        self.late: list[tuple[str, dict[str, Any]]] = []

    def take(self, candidate: str) -> str:
        n = self.seen[candidate] = self.seen.get(candidate, 0) + 1
        return candidate if n == 1 else f"{candidate}~{n}"

    def take_late(self, candidate: str, fact: dict[str, Any]) -> dict[str, Any]:
        """Queue `fact` for the second pass; its `id` stays None until `flush`."""
        self.late.append((candidate, fact))
        return fact

    def flush(self, facts: Any = None) -> Any:
        """The second pass: the queued facts take their ids, in queue order; returns `facts` unchanged."""
        for candidate, fact in self.late:
            fact["id"] = self.take(candidate)
        self.late = []
        return facts
