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


class StoreIOLock:
    def __init__(self, store_path: Path):
        self.store_path = store_path

    @contextlib.contextmanager
    def acquire(self, wait: bool = False):
        lock_file = lock_path(self.store_path)
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            self._lock(lock_fd, wait)
            yield
            fcntl.lockf(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)

    def _lock(self, lock_fd: int, wait: bool):
        flags = fcntl.LOCK_EX
        if not wait:
            flags |= fcntl.LOCK_NB
        try:
            fcntl.lockf(lock_fd, flags)
        except BlockingIOError:
            from sldb.store.exceptions import SLDBStoreError
            raise SLDBStoreError(f"Store at {self.store_path} is busy. Use --wait to block.")
