from __future__ import annotations

from sldb.core.contracts import Marker


def parse_marker(inner: str) -> Marker:
    """
    Parses a marker string into its components.

    Args:
        inner: The content inside ⸢...⸥.

    Returns:
        A Marker model instance.
    """
    head, _, prop = inner.partition("•")
    parts = [part.strip() for part in head.split(",") if part.strip()]
    kind = parts[0] if parts else "rev"
    traits = parts[1:] if parts else []
    name = prop.strip() if prop else ""
    return Marker(kind=kind, traits=traits, name=name)
