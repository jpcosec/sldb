"""The store-side seam: backend names, and the networkx factory that builds one.

A store package cannot import `sldb.api`; resolving a store's `.sldb/store.yaml` therefore
lives above, in `sldb.api.graph.analyze.backend_for`, which reads the declaration and passes
the name here. See `docs/architecture/graph-backend.md`.
"""

from __future__ import annotations

from sldb.store.graph.backend.networkx_backend import NetworkXBackend
from sldb.store.graph.backend.protocol import GraphBackend

DEFAULT_BACKEND = "networkx"
ADMITTED_BACKENDS = (DEFAULT_BACKEND,)


def make_backend(name: str) -> GraphBackend:
    """Build the backend named by `graph_backend`; anything but networkx is rejected."""
    if name == DEFAULT_BACKEND:
        return NetworkXBackend()
    raise ValueError(f'graph_backend {name} no admitido; admitidos: ["networkx"]')


__all__ = [
    "ADMITTED_BACKENDS",
    "DEFAULT_BACKEND",
    "GraphBackend",
    "NetworkXBackend",
    "make_backend",
]
