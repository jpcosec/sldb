"""Locate the source file that defines a registered model, following re-export modules.

`resolve_definition` and `draft_path` moved here from `sldb.cli.commands.model_source` and
`sldb.cli.commands.models_utils`, which re-export them.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.store.io import load_store_index


def draft_path(path: Path) -> Path:
    """The `.temp` sibling of a model source file where its draft lives."""
    return path.with_name(path.name + ".temp")


def resolve_definition(path: Path, module: str, attribute: str, pythonpath: str | None) -> tuple[Path, str, str]:
    """Keep local definitions; follow import references only for re-export modules."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    if any(isinstance(node, ast.ClassDef) and node.name == attribute.split(".")[0] for node in tree.body):
        return path.resolve(), module, attribute
    model = resolve_model_ref(f"{module}:{attribute}", pythonpath)
    return Path(inspect.getfile(model)).resolve(), model.__module__, model.__qualname__


def locate_model_source(store: str | Path | None, model_name: str, pythonpath: str | None = None) -> ModelSource:
    """Find the file and class that define a registered model.

    Args:
        store: The store registering the model (path, alias, or None to discover it).
        model_name: Registered model name.
        pythonpath: Directory to import re-export modules from; defaults to the project root.

    Returns:
        The defining source file, module and attribute path.

    Raises:
        SLDBModelError: When the model is not registered.
    """
    location = open_store(store)
    m_entry = next((m for m in load_store_index(location.store_path).models if m.name == model_name), None)
    if not m_entry:
        raise SLDBModelError(f"Model '{model_name}' not found.")
    mod, attr = m_entry.model_ref.split(":", 1)
    importable_from = pythonpath or str(location.project_root)
    model_path = _recorded_path(m_entry.path, location.project_root) or _imported_path(m_entry, importable_from, location.store_path)
    path, module_name, attr_path = resolve_definition(model_path, mod, attr, importable_from)
    return ModelSource(path=path, module_name=module_name, attr_path=attr_path)


def _recorded_path(recorded: str, root: Path) -> Path | None:
    """The source file the store recorded, when it is one here: a store copied without its
    models, an absolute path from another machine, or an inherited model (no path) is not."""
    if not recorded:
        return None
    path = Path(recorded) if Path(recorded).is_absolute() else root / recorded
    return path if path.is_file() else None


def _imported_path(m_entry, pythonpath: str, store_path: Path) -> Path:
    """Where the class is defined, found by importing `model_ref`."""
    try:
        return Path(inspect.getfile(resolve_model_ref(m_entry.model_ref, pythonpath))).resolve()
    except (SLDBModelError, TypeError, OSError) as exc:
        raise SLDBModelError(f"Model '{m_entry.name}' of store {store_path}: its recorded source '{m_entry.path}' is not a file here and '{m_entry.model_ref}' does not import ({exc}). Pass --pythonpath to where its package lives.") from exc
