"""Per-document shards for the semantic and sections indexes (PLAN 15 capa 5): one small file
per document under `.sldb/runtime/{semantic,sections}/<Model>/<doc>.yaml` instead of one file
for the whole store, so a write touches only its own shard. Each shard carries the `hash_c`
it was built from. Loads are cached by (path, mtime, size) — its own small cache, not
`sldb.store.io`'s (that module imports this one; importing back would be circular)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, TypeVar

from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load
from sldb.store.models import DocSections, SemanticDocumentRecord

T = TypeVar("T")

_SHARDS: dict[str, tuple[tuple, Any]] = {}


def _signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


def _cached_shard(path: Path, loader: Callable[[], T]) -> T:
    key = str(path)
    sig = _signature(path)
    hit = _SHARDS.get(key)
    if hit is None or hit[0] != sig:
        hit = (sig, loader())
        _SHARDS[key] = hit
    return hit[1]


def _forget_shard(path: Path) -> None:
    _SHARDS.pop(str(path), None)


def invalidate_shard_cache() -> None:
    _SHARDS.clear()


def load_semantic_shard(path: Path) -> SemanticDocumentRecord | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: SemanticDocumentRecord(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_semantic_shard(path: Path, record: SemanticDocumentRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    StoreIOUtils._atomic_write(path, yaml_dump(record.model_dump()))
    _SHARDS[str(path)] = (_signature(path), record)


def load_sections_shard(path: Path) -> DocSections | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: DocSections(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_sections_shard(path: Path, doc_sections: DocSections) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    StoreIOUtils._atomic_write(path, yaml_dump(doc_sections.model_dump()))
    _SHARDS[str(path)] = (_signature(path), doc_sections)


def delete_shard(path: Path) -> None:
    path.unlink(missing_ok=True)
    _forget_shard(path)


def list_shard_names(shards_dir: Path) -> list[str]:
    if not shards_dir.is_dir():
        return []
    return sorted(p.stem for p in shards_dir.glob("*.yaml"))


def prune_shards(shards_dir: Path, current_names: set) -> None:
    """Delete every shard whose document is no longer tracked (PLAN 15 capa 5: a document
    untracked or deleted loses its semantic/sections shard right away, not just its entry
    in an aggregate that happens to get rebuilt without it)."""
    for name in list_shard_names(shards_dir):
        if name not in current_names:
            delete_shard(shards_dir / f"{name}.yaml")
