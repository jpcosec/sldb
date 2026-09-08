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

_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # libyaml when present: 7-8x faster on the indexes
_DUMPER = getattr(yaml, "CSafeDumper", yaml.SafeDumper)


def yaml_load(text: str):
    return yaml.load(text, Loader=_LOADER)


def yaml_dump(data) -> str:
    return yaml.dump(data, Dumper=_DUMPER, sort_keys=False, allow_unicode=True)


class StoreIOUtils:
    @staticmethod
    def _atomic_write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = StoreIOUtils._mkstemp(path)
        try:
            StoreIOUtils._write_and_close(fd, content)
            os.replace(tmp_path, path)
        finally:
            StoreIOUtils._cleanup(fd, tmp_path)

    @staticmethod
    def _mkstemp(path: Path):
        return tempfile.mkstemp(
            dir=path.parent, prefix=path.name + ".", suffix=".tmp"
        )

    @staticmethod
    def _write_and_close(fd, content):
        os.write(fd, content.encode("utf-8"))
        os.fsync(fd)
        os.close(fd)

    @staticmethod
    def _cleanup(fd, tmp_path):
        try:
            os.close(fd)
        except OSError:
            pass
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
