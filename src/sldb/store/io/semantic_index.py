import contextlib
import fcntl
import os
import tempfile
from pathlib import Path

import yaml

from sldb.store.layout import (
    lock_path,
    semantic_dag_path,
    semantic_index_path,
    store_index_path,
)
from sldb.store.models import (
    DocumentsIndex,
    ModelsIndex,
    SectionsIndex,
    SemanticDAG,
    SemanticIndex,
    StoreIndex,
)

_LOCK_TIMEOUT = 10

from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load


def _load_legacy_semantic_index(legacy: Path) -> SemanticIndex:
    data = yaml_load(legacy.read_text(encoding="utf-8")) or {}
    return SemanticIndex(**data)


def _invert_tags(documents: dict) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for name, rec in documents.items():
        for tag in rec.tags:
            tags.setdefault(tag, []).append(name)
    return {t: sorted(d) for t, d in tags.items()}


class SemanticIndexIO:
    @staticmethod
    def load(store_path: Path) -> SemanticIndex:
        """Composed from per-document shards (PLAN 15 capa 5); a store not migrated to
        shards yet (no shards, the legacy file still there) reads that file instead —
        `migrate_store_layout` is what shards it, on the next call that touches this store."""
        from sldb.store.io.shard_compose import compose_semantic_documents

        documents = compose_semantic_documents(store_path)
        legacy = semantic_index_path(store_path)
        if not documents and legacy.exists():
            return _load_legacy_semantic_index(legacy)
        return SemanticIndex(tags=_invert_tags(documents), documents=documents)

    @staticmethod
    def save(store_path: Path, index: SemanticIndex) -> None:
        """Shards out every document `index` carries (store_init's empty index, migration's
        one-time conversion of an old store); the fast write path (semantic_doc_contribution)
        writes one shard directly instead of building a whole SemanticIndex for this."""
        from sldb.store.io.shards import save_semantic_shard
        from sldb.store.layout import semantic_shard_path

        for name, rec in index.documents.items():
            save_semantic_shard(semantic_shard_path(store_path, rec.model, name), rec)
        legacy = semantic_index_path(store_path)
        if legacy.exists():
            legacy.unlink()
