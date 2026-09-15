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

class DocumentsIndexIO:
    """`path` is `<store>/core/documents/<model>.yaml` — no longer written to (PLAN 15 capa
    7), still the key every caller already has: the stem is the model name, enough to find
    or make `<store>/core/documents/<model>/`."""

    @staticmethod
    def load(path: Path) -> DocumentsIndex:
        # PLAN 15 capa 8: `entries_of` is this operation's own cache — composed from shards
        # at most once, reused across operations too while the model's hash_b says nothing moved.
        from sldb.store import documents_hash
        from sldb.store.layout import documents_shards_dir, model_name_of_documents_path
        store_path, model_name = path.parent.parent.parent, model_name_of_documents_path(path)
        if documents_shards_dir(store_path, model_name).is_dir():
            return DocumentsIndex(documents=documents_hash.entries_of(store_path, model_name))
        if not path.exists():
            return DocumentsIndex()
        data = yaml_load(path.read_text(encoding="utf-8")) or {}
        return DocumentsIndex(**data)

    @staticmethod
    def save(path: Path, index: DocumentsIndex) -> None:
        from sldb.store.io.shards import save_document_shard
        from sldb.store.layout import documents_shard_path, model_name_of_documents_path

        store_path, model_name = path.parent.parent.parent, model_name_of_documents_path(path)
        for entry in index.documents:
            save_document_shard(documents_shard_path(store_path, model_name, entry.name), entry)
        if path.exists():
            path.unlink()
