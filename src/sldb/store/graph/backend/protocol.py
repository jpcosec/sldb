"""The one seam every graph analysis goes through.

A backend owns an index (the object `compose_edge_index` already produced) and the questions
asked of it. It never hands its internal graph out: callers name an operation and get the
answer, so a future engine can replace networkx without any rule or command seeing it.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class GraphBackend(Protocol):
    """Load a composed index and answer graph questions over it."""

    def load(self, index: Any, projection: dict[str, dict[str, Any] | None] | None = None) -> None:
        """Keep the composed index and the optional `export_id -> facet payload` projection.

        The index is the object `sldb.store.edge_index.compose.compose_edge_index` returns:
        nodes and edges already resolved. Compose is not part of the backend.
        """

    def eval(self, predicate: Any, subject: Any = None) -> list[dict[str, Any]]:
        """Evaluate a parsed predicate on one subject, or over the loaded domain.

        The subject is a payload dict or an `export_id`; the latter is read through the
        projection loaded with `load`. A finding has `node`, `holds`, `clause` and `seen`
        (`docs/architecture/rules-language.md` §4 and §6).
        """

    def analyze(self, op: str, **args: Any) -> Any:
        """Run one whole-graph operation with the arguments it has always received."""
