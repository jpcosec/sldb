"""Write a generated model module under its package and refresh the import cache."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from sldb.api.model_create.model_source import ModelSource


def write_module(source: ModelSource, package: str, pythonpath: str, module_text: str) -> Path:
    """Write the module text, creating the package; return its path."""
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

