"""`load`: un spec YAML a su modelo por tipo."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.loader.any_diagram import ADAPTER, VALID_TYPES
from sldb.models.notation.diagram_specs.loader.read_raw import read_raw
from sldb.models.notation.diagram_specs.loader.schema_error import schema_error
from sldb.notations.exceptions import ParseError


def load(path: str | Path) -> BaseDiagram:
    path = Path(path)
    raw = read_raw(path)
    diagram_type = raw.get("type", "")
    if diagram_type not in VALID_TYPES:
        raise ParseError(f"Unsupported diagram type: {diagram_type}")
    try:
        return ADAPTER.validate_python(raw)
    except PydanticValidationError as exc:
        raise schema_error(exc, path, diagram_type) from exc
