"""Compatibility bridge: model resolution now lives in `sldb.api.model_registry`.

`registered_model` keeps its tuple-returning signature for existing importers (sldb CLI
commands, deskops, kgdb, pron); new code should call `sldb.api.load_registered_model`.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import _get_module, _import_module_attr, _setup_sys_path, resolve_model_ref  # noqa: F401

def registered_model(store_path: Path, model_name: str, pythonpath: str | None) -> tuple[type, Any, Any]:
    """(model class, model entry, store index) of a registered or federated model name."""
    registered = load_registered_model(store_path, model_name, pythonpath)
    return registered.model_type, registered.entry, registered.store_index
