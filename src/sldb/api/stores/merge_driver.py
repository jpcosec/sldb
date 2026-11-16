"""`sldb stores merge-driver %O %A %B %P`: git's custom merge driver for a store's files.

A derived index (`core/store_index.yaml`, `core/models/*.yaml`) keeps the current branch's
version (`%A`), with the store index also registering what only the other branch registered;
its hashes are put right afterwards by `sldb stores rebuild-index`. `store.yaml` joins both
branches' `include` rules (and links, models and predicates). Any other file is a real
conflict: exit 1 and git marks it as usual."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

import yaml

from sldb.api.stores.store_file_merge import merge_declaration_data, merge_index_data
from sldb.store.io.utils import yaml_dump, yaml_load


def store_file_kind(merged_path: str) -> str | None:
    """`index`, `model`, `declaration`, or None for a file this driver does not merge."""
    parts = PurePosixPath(merged_path).parts
    if parts[-2:] == ("core", "store_index.yaml"):
        return "index"
    if len(parts) >= 3 and parts[-3:-1] == ("core", "models") and parts[-1].endswith(".yaml"):
        return "model"
    if parts[-1:] == ("store.yaml",) and len(parts) >= 2 and parts[-2].startswith(".sldb"):
        return "declaration"
    return None


def merge_driver(base: str, current: str, other: str, merged_path: str) -> int:
    """Leave the merge result in `current` (`%A`); 0 resolved, 1 a conflict git must mark."""
    kind = store_file_kind(merged_path)
    if kind is None:
        return 1
    if kind == "model":
        return 0
    return _merge_into(Path(current), Path(other), kind)


def _merge_into(current: Path, other: Path, kind: str) -> int:
    ours, theirs = _load(current), _load(other)
    if ours is None or theirs is None:
        return 0 if kind == "index" else 1  # an unreadable index: rebuild-index repairs it
    merged = merge_index_data(ours, theirs) if kind == "index" else merge_declaration_data(ours, theirs)
    if merged != ours:
        current.write_text(_dump(merged, kind), encoding="utf-8")
    return 0


def _dump(data: dict, kind: str) -> str:
    """Each file in the layout its own writer uses (`StoreIndexIO`, `save_declaration`)."""
    if kind == "index":
        return yaml_dump(data)
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)


def _load(path: Path) -> dict | None:
    try:
        data = yaml_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None
