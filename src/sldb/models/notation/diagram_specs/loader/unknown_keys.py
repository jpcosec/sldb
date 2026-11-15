"""`unknown_keys`: las claves que el esquema no declara."""

from __future__ import annotations

from pydantic import ValidationError as PydanticValidationError

from sldb.models.notation.diagram_specs.loader.any_diagram import VALID_TYPES


def _path_of(err: dict) -> str:
    loc = [str(p) for p in err.get("loc", ())]
    if loc and loc[0] in VALID_TYPES:   # the discriminated union puts the type first
        loc = loc[1:]
    return ".".join(loc)


def unknown_keys(exc: PydanticValidationError) -> list[str]:
    """The dotted path of every key the schema does not declare (``extra_forbidden``), without the
    tag of the diagram union: ``data.edges``, ``data.nodes.ec2.estado``, ``data.connections.0.via``."""
    return [_path_of(err) for err in exc.errors() if err.get("type") == "extra_forbidden"]
