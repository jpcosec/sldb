"""Generate a model module from its declaration: base resolution, rendering, check, write."""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_create.model_source import ModelSource
from sldb.api.model_create.module_writing import write_module
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.core.exceptions import SLDBModelError


def generate_model(
    sp: Path,
    name: str,
    fields: list,
    template: str | None,
    base: str | None,
    package: str,
    pythonpath: str,
    containment: dict[str, list[str]] | None = None,
    references: list[str] | None = None,
    compositions: dict[str, dict] | None = None,
    semantics: dict[str, list[str]] | None = None,
    authority: str | None = None,
) -> tuple[Path, str, ModelSource]:
    """Resolve the base, render and check the module, write it; return its path, ref and source."""
    base_ref, head, inherited_fields = resolve_base(sp, base, pythonpath)
    extras = {"containment": containment, "references": references, "compositions": compositions, "semantics": semantics, "authority": authority}
    source = ModelSource.of(name, fields, template, base_ref, inherited_fields=inherited_fields, **extras)
    module_text = source.module(head)
    _require_working(module_text, name)
    path = write_module(source, package, pythonpath, module_text)
    return path, f"{package}.{source.snake}:{name}", source


def _require_working(module_text: str, name: str) -> None:
    """Refuse a generated module that does not import and roundtrip."""
    check = ModelCheck(module_text, name)()
    if not check["ok"]:
        raise SLDBModelError(f"The generated model {name} does not work: {'; '.join(check['errors'])}")


def resolve_base(sp: Path, base: str | None, pythonpath: str) -> tuple[tuple[str, str], str | None, set[str]]:
    """The base's (module, class), the head of its template and the field names it brings."""
    if base is None:
        return ("sldb", "StructuredNLDoc"), None, set()
    cls = load_registered_model(sp, base, pythonpath).model_type
    head = str(getattr(cls, "__template__", "")).strip() or None
    return (cls.__module__, cls.__name__), head, set(cls.model_fields.keys())
