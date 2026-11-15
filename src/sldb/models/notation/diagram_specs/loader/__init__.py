"""Carga de un spec de diagrama a su modelo por tipo."""

from sldb.models.notation.diagram_specs.loader.any_diagram import ADAPTER, VALID_TYPES, AnyDiagram
from sldb.models.notation.diagram_specs.loader.load import load
from sldb.models.notation.diagram_specs.loader.unknown_keys import unknown_keys

__all__ = ["load", "unknown_keys", "AnyDiagram", "ADAPTER", "VALID_TYPES"]
