"""Move a pre-`.sldb/core` store's indexes to where every reader looks today.

A store from before the `core/` and `runtime/` split keeps `store_index.yaml`,
`semantic_index.yaml`, `semantic_dag.yaml`, `models/<M>.yaml` and `documents/<M>.yaml`
at the store root. Nothing reads that shape any more, and `migrate_store_layout` starts
by loading `core/store_index.yaml`, so `open_store` crashed on such a store before ever
reaching the shard migration. This relocation rewrites the paths the indexes name and
moves the files next to them; the shard migration then sees an ordinary store. Only the
paths move — the old hash key names are the models' validation aliases, rewritten on the
next save.
"""

from __future__ import annotations

import contextlib
import shutil
from pathlib import Path

from sldb.store.io import save_store_index
from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load
from sldb.store.layout import (
    documents_index_relpath,
    legacy_semantic_dag_path,
    legacy_semantic_index_path,
    legacy_store_index_path,
    models_index_relpath,
    sections_index_relpath,
    semantic_dag_path,
    semantic_index_path,
    store_index_path,
)
from sldb.store.models import StoreIndex


def relocate_legacy_layout(store_path: Path, project_root: Path) -> bool:
    """Move a root-level legacy layout to the canonical paths; False when there is none."""
    if store_index_path(store_path).exists() or not legacy_store_index_path(store_path).exists():
        return False
    data = _read_yaml(legacy_store_index_path(store_path))
    for model in data.get("models") or []:
        _relocate_model(model, store_path, project_root)
    save_store_index(store_path, StoreIndex(**data))
    _relocate_root_files(store_path)
    return True


def _relocate_root_files(store_path: Path) -> None:
    """Move the store-wide legacy files next to their canonical paths and drop the old dirs."""
    _move(legacy_semantic_index_path(store_path), semantic_index_path(store_path))
    _move(legacy_semantic_dag_path(store_path), semantic_dag_path(store_path))
    legacy_store_index_path(store_path).unlink()
    _prune(store_path / "models")
    _prune(store_path / "documents")


def _relocate_model(model: dict, store_path: Path, project_root: Path) -> None:
    """Move one model's index files to their canonical paths, rewriting the links it holds."""
    source = project_root / model["models_index"]
    index = _read_yaml(source) if source.exists() else {}
    _relocate_child(index, "documents_index", documents_index_relpath(store_path, model["name"]), project_root)
    if index.get("sections_index"):
        _relocate_child(index, "sections_index", sections_index_relpath(store_path, model["name"]), project_root)
    model["models_index"] = models_index_relpath(store_path, model["name"])
    _write_yaml(project_root / model["models_index"], index)
    with contextlib.suppress(OSError):
        source.unlink()


def _relocate_child(index: dict, key: str, canonical_rel: str, project_root: Path) -> None:
    """Move the file `index[key]` names to `canonical_rel`, then point the key at the new path."""
    if index.get(key):
        _move(project_root / index[key], project_root / canonical_rel)
        index[key] = canonical_rel


def _read_yaml(path: Path) -> dict:
    return yaml_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, data: dict) -> None:
    StoreIOUtils._atomic_write(path, yaml_dump(data))


def _move(source: Path, destination: Path) -> None:
    """Relocate a legacy index file that exists; a missing source is a store without it."""
    if not source.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))


def _prune(directory: Path) -> None:
    """Remove a legacy directory once each file it held has been relocated."""
    with contextlib.suppress(OSError):
        directory.rmdir()
