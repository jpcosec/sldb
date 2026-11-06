"""Generate a model from a JSON declaration, check it, write it and register it.

`sldb.api.create_model` is the substrate operation behind pron's `kb_model_create`: it
turns `[{name, type, description, required?, default?, enum?}]` into a `StructuredNLDoc`
module under `<pythonpath>/<target_package>/`, refuses a module that does not import and
roundtrip, and registers it.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_create.model_source import ModelSource
from sldb.api.model_registry.add_model import add_model
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError

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
    _path, ref, _source = _generate(
        location.store_path,
        name,
        fields,
        template,
        base,
        target_package,
        pythonpath,
        containment=containment,
        references=references,
        compositions=compositions,
        semantics=semantics,
        authority=authority,
    )
    return add_model(location.store_path, ref, pythonpath, actor=actor)


def _generate(
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
    base_ref, head, inherited_fields = _resolve_base(sp, base, pythonpath)
    source = ModelSource.of(
        name,
        fields,
        template,
        base_ref,
        containment=containment,
        references=references,
        compositions=compositions,
        semantics=semantics,
        authority=authority,
        inherited_fields=inherited_fields,
    )
    module_text = source.module(head)
    check = ModelCheck(module_text, name)()
    if not check["ok"]:
        raise SLDBModelError(f"The generated model {name} does not work: {'; '.join(check['errors'])}")
    path = _write_module(source, package, pythonpath, module_text)
    return path, f"{package}.{source.snake}:{name}", source


def _resolve_base(sp: Path, base: str | None, pythonpath: str) -> tuple[tuple[str, str], str | None, set[str]]:
    if base is None:
        return ("sldb", "StructuredNLDoc"), None, set()
    cls = load_registered_model(sp, base, pythonpath).model_type
    head = str(getattr(cls, "__template__", "")).strip() or None
    return (cls.__module__, cls.__name__), head, set(cls.model_fields.keys())


def _write_module(source: ModelSource, package: str, pythonpath: str, module_text: str) -> Path:
    parts = package.split(".")
    dir_path = Path(pythonpath, *parts)
    dir_path.mkdir(parents=True, exist_ok=True)
    _touch_init(Path(pythonpath), parts)
    path = dir_path / f"{source.snake}.py"
    path.write_text(module_text, encoding="utf-8")
    _forget(package, pythonpath)
    return path


def _touch_init(root: Path, parts: list[str]) -> None:
    for i in range(1, len(parts) + 1):
        (Path(root, *parts[:i]) / "__init__.py").touch()


def _forget(package: str, pythonpath: str) -> None:
    """Drop the generated package from the import cache so the new module is found."""
    if pythonpath not in sys.path:
        sys.path.insert(0, pythonpath)
    importlib.invalidate_caches()
    root = package.split(".")[0]
    for key in [k for k in sys.modules if k == root or k.startswith(root + ".")]:
        del sys.modules[key]

