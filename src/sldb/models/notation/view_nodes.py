"""Normaliza las entradas `{model, where}` de los nodos de una `ViewDoc`."""

from __future__ import annotations


def _view_node(entry):
    """Una entrada validada como `{model, where}`."""
    if not isinstance(entry, dict) or not entry.get("model"):
        raise ValueError(f"each view node entry needs a model: {entry!r}")
    unknown = set(entry) - {"model", "where"}
    if unknown:
        raise ValueError(f"view node entries only take model and where, got {sorted(unknown)}")
    return {"model": str(entry["model"]), "where": str(entry.get("where") or "")}


def normalize_view_nodes(value):
    """Las entradas de `nodes` normalizadas; None es la lista vacia."""
    return [] if value is None else [_view_node(entry) for entry in value]
