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

class StoreIndexIO:
    @staticmethod
    def load(store_path: Path) -> StoreIndex:
        index_file = store_index_path(store_path)
        if not index_file.exists():
            raise FileNotFoundError(f"No store_index.yaml at {store_path}")
        data = yaml_load(index_file.read_text(encoding="utf-8")) or {}
        return StoreIndex(**data)

    @staticmethod
    def save(store_path: Path, index: StoreIndex) -> None:
        StoreIOUtils._atomic_write(
            store_index_path(store_path),
            yaml_dump(index.model_dump()),
        )
