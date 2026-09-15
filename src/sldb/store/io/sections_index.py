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

class SectionsIndexIO:
    """`path` is `<store>/runtime/sections/<model>.yaml` — no longer written to (PLAN 15 capa
    5), still the key every caller already has: three parents up is the store, the stem is
    the model name, and that is enough to find or make `<store>/runtime/sections/<model>/`."""

    @staticmethod
    def load(path: Path) -> SectionsIndex:
        from sldb.store.io.shard_compose import compose_sections_documents
        from sldb.store.layout import model_name_of_sections_path, sections_shards_dir

        store_path, model_name = path.parent.parent.parent, model_name_of_sections_path(path)
        if sections_shards_dir(store_path, model_name).is_dir():
            return SectionsIndex(documents=compose_sections_documents(store_path, model_name))
        if not path.exists():
            return SectionsIndex()
        data = yaml_load(path.read_text(encoding="utf-8")) or {}
        return SectionsIndex(**data)

    @staticmethod
    def save(path: Path, index: SectionsIndex) -> None:
        from sldb.store.io.shards import save_sections_shard
        from sldb.store.layout import model_name_of_sections_path, sections_shard_path

        store_path, model_name = path.parent.parent.parent, model_name_of_sections_path(path)
        for doc in index.documents:
            save_sections_shard(sections_shard_path(store_path, model_name, doc.doc_name), doc)
        if path.exists():
            path.unlink()

