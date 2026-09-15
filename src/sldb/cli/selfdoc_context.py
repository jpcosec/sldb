"""Resolve self-documentation roots without migrating during reads."""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from sldb.cli.store_context import _find_default_store, _resolve_store_arg
from sldb.store.layout import project_root, store_exists, store_index_path


def documentation_store(store_arg: str | None) -> tuple[Path, Path]:
    """Find a canonical store; check and scan must not migrate it implicitly."""
    store = _resolve_store_arg(store_arg) if store_arg else _find_default_store("readonly")
    if not store_exists(store) or not store_index_path(store).exists():
        raise ValueError(f"Canonical store required at {store}; initialize or migrate it first")
    return store, project_root(store)


def load_parser(factory_ref: str, root: Path, pythonpath: str | None) -> argparse.ArgumentParser:
    """Load a trusted parser factory and build its tree without dispatching handlers."""
    location = Path(pythonpath) if pythonpath else root
    location = location if location.is_absolute() else root / location
    for entry in (str(root), str(location.resolve())):
        if entry not in sys.path:
            sys.path.insert(0, entry)
    module, separator, name = factory_ref.partition(":")
    if not separator:
        raise ValueError("Parser factory must use module:callable syntax")
    return _build_parser(importlib.import_module(module), name)


def _build_parser(module, name: str) -> argparse.ArgumentParser:
    factory = module
    for part in name.split("."):
        factory = getattr(factory, part)
    parser = factory()
    if not isinstance(parser, argparse.ArgumentParser):
        raise ValueError("Parser factory must return argparse.ArgumentParser")
    return parser
