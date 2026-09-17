"""Per-document shards for the semantic, sections and edges indexes (PLAN 15 capa 5): one small file
per document under `.sldb/runtime/{semantic,sections,edges}/<Model>/<doc>.yaml` instead of one file
for the whole store, so a write touches only its own shard. Each shard carries the `hash_c`
it was built from. Loads are cached by (path, mtime, size) — its own small cache, not
`sldb.store.io`'s (that module imports this one; importing back would be circular)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, TypeVar

from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load
from sldb.store.models import DocSections, DocumentEntry, EdgeContribution, SemanticDocumentRecord

T = TypeVar("T")
E = TypeVar("E", bound=EdgeContribution)

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


def _save_shard(path: Path, value: Any, loader: Callable[[], T]) -> None:
    """Write only when the content differs from the shard already there (the same "leave the
    file alone" guarantee the single-file indexes always gave): a rebuild or a re-save of the
    same value costs a read of the cached/on-disk shard, not a write."""
    if path.exists() and _cached_shard(path, loader) == value:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    StoreIOUtils._atomic_write(path, yaml_dump(value.model_dump()))
    _SHARDS[str(path)] = (_signature(path), value)


def load_semantic_shard(path: Path) -> SemanticDocumentRecord | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: SemanticDocumentRecord(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_semantic_shard(path: Path, record: SemanticDocumentRecord) -> None:
    _save_shard(path, record, lambda: SemanticDocumentRecord(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def load_sections_shard(path: Path) -> DocSections | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: DocSections(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_sections_shard(path: Path, doc_sections: DocSections) -> None:
    _save_shard(path, doc_sections, lambda: DocSections(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def load_edges_shard(path: Path, shard_type: type[E]) -> E | None:
    """An edges shard of the given shape: DocEdges, ModelEdges, or the store's EdgeContribution."""
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: shard_type(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_edges_shard(path: Path, shard: EdgeContribution) -> None:
    _save_shard(path, shard, lambda: type(shard)(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def load_document_shard(path: Path) -> DocumentEntry | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: DocumentEntry(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_document_shard(path: Path, entry: DocumentEntry) -> None:
    _save_shard(path, entry, lambda: DocumentEntry(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


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
