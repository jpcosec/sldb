"""`schema_error`: el `ParseError` de un spec que no cumple el esquema de su tipo."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from sldb.models.notation.diagram_specs.loader.unknown_keys import unknown_keys
from sldb.notations.exceptions import ParseError


def schema_error(exc: PydanticValidationError, path: Path, diagram_type: str) -> ParseError:
    desconocidas = unknown_keys(exc)
    if not desconocidas:
        return ParseError(f"Invalid diagram schema in {path}: {exc}")
    listado = "; ".join(f"unknown key '{k}'" for k in desconocidas)
    return ParseError(f"Invalid diagram schema in {path} (type {diagram_type}): {listado}. "
                      "Every key must be part of the schema of its type "
                      "(`spec2viz diagram schema` exports them).")
