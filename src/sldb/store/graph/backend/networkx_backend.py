"""The networkx implementation of the `GraphBackend` seam.

It wraps `sldb.store.graph.analysis` unchanged: every operation receives the composed index
and returns what the analysis returned. The index is kept private; callers only ask for an
operation by name. `eval` is the whole predicate language of GO05 (paths included) over the
index's graph view (`index_view`), on a payload, an `export_id` read through the projection,
or the whole domain.

The seam exists so that a future engine (Kùzu, Neo4j, Datalevin) can sit behind the same three
methods. See `docs/architecture/graph-backend.md`.
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.graph import analysis
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import findings, node_finding
from sldb.store.graph.language.predicate_view import node, with_node

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
        """`eval(predicate, subject)` of rules-language.md §6 over the loaded index: the
        subject's finding (a payload, or an export id read through the projection), or, with
        no subject, one per document of the domain. Paths read the index's edges."""
        view = index_view(self._index, self._projection)
        if subject is None:
            return findings(predicate, view)
        item = self._subject(view, subject)
        return [node_finding(predicate, with_node(view, item), item)]

    def _subject(self, view: dict[str, Any], subject: Any) -> dict[str, Any]:
        if isinstance(subject, str):
            return {**(view["node"](subject) or node(subject, None, {})), "payload": self._projected(subject)}
        if isinstance(subject, dict):
            return self._payload_subject(view, subject)
        raise TypeError("el sujeto de eval es un payload (dict) o un export_id (str)")

    def _payload_subject(self, view: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        node_id = str(payload.get("id") or payload.get("name") or "")
        known = view["node"](node_id)
        if known is not None:
            return {**known, "payload": payload}
        return node(node_id, payload.get("model"), payload, payload.get("base_models") or ())

    def _projected(self, export_id: str) -> dict[str, Any]:
        if self._projection is None or export_id not in self._projection:
            raise ValueError(f"sin proyección para {export_id}")
        return self._projection[export_id] or {}
