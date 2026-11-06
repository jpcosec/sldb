"""Validation of a model declaration: its fields and the field names its attributes cite."""

from __future__ import annotations

import re

from sldb.api.model_create.field_decl import FieldDecl
from sldb.core.exceptions import SLDBModelError


def declared_fields(name: str, fields: list) -> tuple[FieldDecl, ...]:
    """The declared fields as FieldDecl; the name must be CamelCase and the fields unique."""
    if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", name or ""):
        raise SLDBModelError(f"model name {name!r} is not a CamelCase identifier")
    decls = tuple(FieldDecl.of(f) for f in fields or [])
    if not decls:
        raise SLDBModelError("a model needs at least one field")
    if len({d.name for d in decls}) < len(decls):
        raise SLDBModelError("two fields with the same name")
    return decls


def check_field_names(attr: str, cited: list | dict | None, known: set[str], model: str) -> None:
    """Every field named by containment or references must exist in the model."""
    for f in cited or []:
        if f not in known:
            raise SLDBModelError(f"Field '{f}' in {attr} does not exist in model '{model}'.")


def check_compositions(compositions: dict | None, known: set[str], template: str | None) -> None:
    """Each composition names a known source field and, with a template, its render marker."""
    for comp_name, spec in (compositions or {}).items():
        if not isinstance(spec, dict):
            raise SLDBModelError(f"Composition '{comp_name}' must be a dict.")
        src = spec.get("source_field")
        if not src or src not in known:
            raise SLDBModelError(f"Composition '{comp_name}' references unknown source field '{src}'.")
        if template is not None and f"⸢render•{comp_name}⸥" not in template:
            raise SLDBModelError(f"Composition '{comp_name}' requires marker '⸢render•{comp_name}⸥' in template.")
