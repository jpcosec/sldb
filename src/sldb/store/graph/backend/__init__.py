"""Which `GraphBackend` a store uses: `.sldb/store.yaml`'s `graph_backend`, networkx default."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_declaration import declaration_path, load_declaration
from sldb.store.graph.backend.networkx_backend import NetworkXBackend
from sldb.store.graph.backend.protocol import GraphBackend

DEFAULT_BACKEND = "networkx"
ADMITTED_BACKENDS = (DEFAULT_BACKEND,)


def backend_for(store_path: str | Path | None = None) -> GraphBackend:
    """The backend the store declares; an absent declaration or key means networkx."""
    return make_backend(declared_backend_name(store_path))


def declared_backend_name(store_path: str | Path | None = None) -> str:
    """The `graph_backend` value of the store's declaration, or the default when it has none."""
    if store_path is None:
        return DEFAULT_BACKEND
    path = Path(store_path)
    if path.name != ".sldb" and (path / ".sldb").is_dir():
        path = path / ".sldb"
    if not declaration_path(path).is_file():
        return DEFAULT_BACKEND
    return load_declaration(path).graph_backend


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
    "backend_for",
    "declared_backend_name",
    "make_backend",
]
