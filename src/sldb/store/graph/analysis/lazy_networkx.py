"""`networkx` loaded on first use (H11b): importing it costs ~0.09 s, and a command that never
analyses a graph (`sldb views run`, every `sldb --help`) should not pay it. Used as `nx`."""

from __future__ import annotations

from typing import Any


class _LazyNetworkx:
    def __getattr__(self, name: str) -> Any:
        import networkx

        return getattr(networkx, name)


nx = _LazyNetworkx()
