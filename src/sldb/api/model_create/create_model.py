"""Generate a model from a JSON declaration, check it, write it and register it.

`sldb.api.create_model` is the substrate operation behind pron's `kb_model_create`: it
turns `[{name, type, description, required?, default?, enum?}]` into a `StructuredNLDoc`
module under `<pythonpath>/<target_package>/`, refuses a module that does not import and
roundtrip, and registers it.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_create.model_generation import generate_model
from sldb.api.model_registry.add_model import add_model
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store

DEFAULT_PACKAGE = "sldb_generated"


def create_model(
    store: str | Path | None,
    name: str,
    fields: list,
    template: str | None = None,
    base: str | None = None,
    target_package: str = DEFAULT_PACKAGE,
    pythonpath: str | None = None,
    actor: str | None = None,
    containment: dict[str, list[str]] | None = None,
    references: list[str] | None = None,
    compositions: dict[str, dict] | None = None,
    semantics: dict[str, list[str]] | None = None,
    authority: str | None = None,
) -> ModelRegistration:
    """Generate, check, write and register a model declared as JSON fields.

    Args:
        store: The store to register the model in (path, alias, or None to discover it).
        name: CamelCase model name; the class and file name derive from it.
        fields: List of `{name, type, description, required?, default?, enum?}` dicts.
        template: The model's Markdown template; None renders one section per field.
        base: A registered model name the new model extends; None extends StructuredNLDoc.
        target_package: Package under `pythonpath` to write the generated module into.
        pythonpath: Directory importing the module from; defaults to the store's project root.
        actor: Optional caller label; accepted for compatibility, no longer recorded (the journal was retired on 2026-11-04).
        containment: Visual containment mapping field -> allowed target models.
        references: Fields holding doc ids that are not containment.
        compositions: Compositions mapping name -> spec dict.
        semantics: Semantic mapping for the model.
        authority: Model authority ("generated", "authored", etc.).

    Returns:
        The new registry record (version 1).

    Raises:
        SLDBModelError: When the declaration is invalid or the generated module fails its check.
    """
    location = open_store(store)
    pythonpath = pythonpath or str(location.project_root)
    extras = {"containment": containment, "references": references, "compositions": compositions, "semantics": semantics, "authority": authority}
    _path, ref, _source = generate_model(location.store_path, name, fields, template, base, target_package, pythonpath, **extras)
    return add_model(location.store_path, ref, pythonpath, actor=actor)
