"""Follow public model re-exports when locating an editable class definition."""
from __future__ import annotations

import ast
import inspect
from pathlib import Path
from sldb.cli.model_utils import resolve_model_ref


def resolve_definition(path: Path, module: str, attribute: str, pythonpath: str | None) -> tuple[Path, str, str]:
    """Keep local definitions; follow import references only for re-export modules."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    if any(isinstance(node, ast.ClassDef) and node.name == attribute.split(".")[0] for node in tree.body):
        return path.resolve(), module, attribute
    model = resolve_model_ref(f"{module}:{attribute}", pythonpath)
    return Path(inspect.getfile(model)).resolve(), model.__module__, model.__qualname__
