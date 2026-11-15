"""`load_spec` y `validate_spec`: cargar un spec YAML a su modelo por tipo y validarlo."""

from __future__ import annotations

from pathlib import Path

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.loader import load
from sldb.models.notation.diagram_specs.validator import validate


def load_spec(path: str | Path) -> BaseDiagram:
    """El modelo por tipo de un spec YAML (`ParseError` si no se puede leer o no cumple el esquema)."""
    return load(path)


def validate_spec(model: BaseDiagram) -> None:
    """La validación semántica de un spec cargado (`ValidationError` y sus subclases)."""
    validate(model)
