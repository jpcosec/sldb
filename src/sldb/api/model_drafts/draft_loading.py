"""Load a model class from a draft source file without replacing the imported module.

Moved here from `sldb.cli.commands.models_utils`, which re-exports these names.
"""

from __future__ import annotations

import importlib.util
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import _setup_sys_path as setup_sys_path
from sldb.core.exceptions import SLDBModelDraftError


def load_model_from_path(path: Path, module_name: str, attr_path: str, pythonpath: str | None) -> Any:
    """Execute a model source file as a `<module>__draft__` module and return the class.

    Raises:
        SLDBModelDraftError: When no loader can be built for the file.
    """
    setup_sys_path(pythonpath)
    loader = SourceFileLoader(f"{module_name}__draft__", str(path))
    spec = importlib.util.spec_from_loader(f"{module_name}__draft__", loader)
    if spec is None or spec.loader is None:
        raise SLDBModelDraftError(f"Could not load model draft from {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return extract_attr(module, attr_path)


def extract_attr(obj: Any, attr_path: str) -> Any:
    """Follow a dotted attribute path from an object."""
    for attr in attr_path.split("."):
        obj = getattr(obj, attr)
    return obj
