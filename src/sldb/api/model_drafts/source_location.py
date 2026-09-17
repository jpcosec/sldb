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
    model_path = Path(m_entry.path)
    if not model_path.is_absolute():
        model_path = location.project_root / model_path
    mod, attr = m_entry.model_ref.split(":", 1)
    path, module_name, attr_path = resolve_definition(model_path, mod, attr, pythonpath or str(location.project_root))
    return ModelSource(path=path, module_name=module_name, attr_path=attr_path)
