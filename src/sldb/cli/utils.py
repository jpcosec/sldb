from __future__ import annotations

import sys
from importlib import import_module
import json
from pathlib import Path
from typing import Any

import yaml

from sldb.core.exceptions import SLDBModelError
from sldb.models.structured_doc import StructuredNLDoc


def resolve_model_ref(
    model_ref: str, pythonpath: str | None = None
) -> type[StructuredNLDoc]:
    """Resolve a string reference into a StructuredNLDoc class."""
    if ":" not in model_ref:
        raise SLDBModelError("Model reference must use the form 'module:ClassName'.")

    search_paths = [str(Path.cwd().resolve())]
    if pythonpath:
        search_paths.insert(0, str(Path(pythonpath).resolve()))

    for path in reversed(search_paths):
        if path not in sys.path:
            sys.path.insert(0, path)

    module_name, attr_path = model_ref.split(":", 1)
    try:
        module = import_module(module_name)
    except ImportError as exc:
        raise SLDBModelError(f"Failed to import module '{module_name}'.") from exc

    obj: Any = module
    try:
        for attr in attr_path.split("."):
            obj = getattr(obj, attr)
    except AttributeError as exc:
        raise SLDBModelError(
            f"Attribute '{attr_path}' not found in '{module_name}'."
        ) from exc

    if not isinstance(obj, type) or not issubclass(obj, StructuredNLDoc):
        raise SLDBModelError(f"'{model_ref}' is not a StructuredNLDoc subclass.")

    return obj


def read_text(path: str) -> str:
    """Read text from a file or stdin."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str, content: str) -> None:
    """Write text to a file or stdout."""
    if path == "-":
        sys.stdout.write(content)
        return
    Path(path).write_text(content, encoding="utf-8")


def get_store_context(store_arg: str | None) -> tuple[Path, Path]:
    """Resolve store path and project root."""
    from sldb.store.resolver import find_local_store
    from sldb.core.exceptions import SLDBStoreError

    if store_arg:
        sp = Path(store_arg).resolve()
    else:
        found = find_local_store()
        if not found:
            raise SLDBStoreError("No store found. Run 'sldb store init'.")
        sp = found
    return sp, sp.parent


def registered_model(
    store_path: Path, model_name: str, pythonpath: str | None
) -> tuple[type, Any, Any]:
    """Helper to load a registered model and its store metadata."""
    from sldb.store.io import load_store_index

    idx = load_store_index(store_path)
    entry = next((m for m in idx.models if m.name == model_name), None)
    if entry is None:
        from sldb.core.exceptions import SLDBStoreError

        raise SLDBStoreError(f"Model '{model_name}' not registered.")
    return resolve_model_ref(entry.model_ref, pythonpath), entry, idx


def parse_data_value(raw: str) -> Any:
    """Parse JSON/YAML scalars or objects from a CLI string."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return yaml.safe_load(raw)


def deep_get(payload: Any, path: str) -> Any:
    value = payload
    for part in _split_path(path):
        if isinstance(value, dict):
            if part not in value:
                raise KeyError(path)
            value = value[part]
            continue
        if isinstance(value, list):
            value = value[int(part)]
            continue
        raise KeyError(path)
    return value


def deep_set(payload: Any, path: str, new_value: Any, create: bool = False) -> Any:
    parts = _split_path(path)
    target = payload
    for part in parts[:-1]:
        if isinstance(target, dict):
            if part not in target:
                if not create:
                    raise KeyError(path)
                target[part] = {}
            target = target[part]
            continue
        if isinstance(target, list):
            target = target[int(part)]
            continue
        raise KeyError(path)

    leaf = parts[-1]
    if isinstance(target, dict):
        if not create and leaf not in target:
            raise KeyError(path)
        target[leaf] = new_value
        return payload
    if isinstance(target, list):
        target[int(leaf)] = new_value
        return payload
    raise KeyError(path)


def deep_delete(payload: Any, path: str) -> Any:
    parts = _split_path(path)
    target = payload
    for part in parts[:-1]:
        target = target[part] if isinstance(target, dict) else target[int(part)]
    leaf = parts[-1]
    if isinstance(target, dict):
        target.pop(leaf, None)
        return payload
    if isinstance(target, list):
        target.pop(int(leaf))
        return payload
    raise KeyError(path)


def ensure_list(payload: Any, path: str) -> list[Any]:
    value = deep_get(payload, path)
    if not isinstance(value, list):
        raise TypeError(f"Target '{path}' is not a list field.")
    return value


def _split_path(path: str) -> list[str]:
    parts = [part for part in path.split(".") if part]
    if not parts:
        raise KeyError(path)
    return parts
