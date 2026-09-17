"""Import a model class from its `module:ClassName` reference.

Moved here from `sldb.cli.model_utils`, which re-exports these names for existing importers.
"""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from typing import Any

from sldb.core.exceptions import SLDBModelError
from sldb.models.structured_doc import StructuredNLDoc


def _setup_sys_path(pythonpath: str | None) -> None:
    """Put `pythonpath` (then the working directory) at the front of `sys.path`, once each."""
    search_paths = [str(Path.cwd().resolve())]
    if pythonpath:
        search_paths.insert(0, str(Path(pythonpath).resolve()))
    for path in reversed(search_paths):
        if path not in sys.path:
            sys.path.insert(0, path)


def _get_module(module_name: str) -> Any:
    """Import a module, reporting an import failure as a model error."""
    try:
        return import_module(module_name)
    except ImportError as exc:
        raise SLDBModelError(f"Failed to import module '{module_name}'.") from exc


def _import_module_attr(module_name: str, attr_path: str) -> Any:
    """Follow a dotted attribute path inside an imported module."""
    obj = _get_module(module_name)
    try:
        for attr in attr_path.split("."):
            obj = getattr(obj, attr)
    except AttributeError as exc:
        raise SLDBModelError(f"Attribute '{attr_path}' not found in '{module_name}'.") from exc
    return obj


def resolve_model_ref(model_ref: str, pythonpath: str | None = None) -> type[StructuredNLDoc]:
    """Import the StructuredNLDoc subclass a model reference names.

    Args:
        model_ref: Reference of the form `module:ClassName` (the attribute may be dotted).
        pythonpath: Directory to import the module from, ahead of the working directory.

    Returns:
        The model class.

    Raises:
        SLDBModelError: When the reference is malformed, cannot be imported, or does not
            name a StructuredNLDoc subclass.
    """
    if ":" not in model_ref:
        raise SLDBModelError("Model reference must use the form 'module:ClassName'.")
    _setup_sys_path(pythonpath)
    module_name, attr_path = model_ref.split(":", 1)
    obj = _import_module_attr(module_name, attr_path)
    if not isinstance(obj, type) or not issubclass(obj, StructuredNLDoc):
        raise SLDBModelError(f"'{model_ref}' is not a StructuredNLDoc subclass.")
    return obj
