"""The networkx implementation of the `GraphBackend` seam.

It wraps `sldb.store.graph.analysis` unchanged: every operation receives the composed index
and returns what the analysis returned. The index is kept private; callers only ask for an
operation by name. `eval` implements the GO02 subset without paths, over a payload or an
`export_id` resolved through the projection.

The seam exists so that a future engine (Kùzu, Neo4j, Datalevin) can sit behind the same three
methods. See `docs/architecture/graph-backend.md`.
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.graph import analysis
from sldb.store.graph.backend.eval import evaluate_finding

_OPERATIONS: dict[str, Callable[..., Any]] = {
    "path": analysis.path_between,
    "paths": analysis.paths_between,
    "cycles": analysis.cycles,
    "order": analysis.topological_order,
    "layers": analysis.layers,
    "components": analysis.components,
    "islands": analysis.islands,
    "isolated": analysis.isolated,
    "central": analysis.central,
    "similar": analysis.similar_to,
}


class NetworkXBackend:
    """The current engine: `sldb.store.graph.analysis` over the composed edge index."""

    def __init__(self) -> None:
        self._index: Any = None
        self._projection: dict[str, dict[str, Any] | None] | None = None

    def load(self, index: Any, projection: dict[str, dict[str, Any] | None] | None = None) -> None:
        """Keep the composed index and the optional export-id projection; return nothing."""
        self._index = index
        self._projection = projection
        return None

    def analyze(self, op: str, **args: Any) -> Any:
        """Run one analysis operation with the arguments the analyses already take."""
        if self._index is None:
            raise RuntimeError("GraphBackend.analyze called before load")
        operation = _OPERATIONS.get(op)
        if operation is None:
            raise ValueError(f"Unknown graph operation: {op}")
        return operation(self._index, **args)

    def eval(self, predicate: Any, subject: Any = None) -> list[dict[str, Any]]:
        """Evaluate a parsed predicate on a payload or export id, or over the projection."""
        if subject is None:
            return self._eval_domain(predicate)
        payload, node = self._subject(subject)
        return [evaluate_finding(predicate, payload, node)]

    def _subject(self, subject: Any) -> tuple[dict[str, Any], str]:
        if isinstance(subject, str):
            return self._projected(subject), subject
        if isinstance(subject, dict):
            return subject, str(subject.get("id") or subject.get("name") or "")
        raise TypeError("el sujeto de eval es un payload (dict) o un export_id (str)")

    def _projected(self, export_id: str) -> dict[str, Any]:
        if self._projection is None or export_id not in self._projection:
            raise ValueError(f"sin proyección para {export_id}")
        return self._projection[export_id] or {}

    def _eval_domain(self, predicate: Any) -> list[dict[str, Any]]:
        if not self._projection:
            return []
        return [evaluate_finding(predicate, payload or {}, export_id) for export_id, payload in sorted(self._projection.items())]
