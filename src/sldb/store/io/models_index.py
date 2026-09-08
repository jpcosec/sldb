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

class ModelsIndexIO:
    @staticmethod
    def load(path: Path) -> ModelsIndex:
        data = yaml_load(path.read_text(encoding="utf-8")) or {}
        return ModelsIndex(**data)

    @staticmethod
    def save(path: Path, index: ModelsIndex) -> None:
        StoreIOUtils._atomic_write(
            path,
            yaml_dump(index.model_dump()),
        )

