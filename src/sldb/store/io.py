import contextlib
import fcntl
import os
import tempfile
from pathlib import Path

import yaml

from sldb.core.exceptions import SLDBStoreError
from sldb.store.models import (
    DocumentsIndex,
    ModelsIndex,
    SectionsIndex,
    SemanticDAG,
    SemanticIndex,
    StoreIndex,
)


_LOCK_TIMEOUT = 10


@contextlib.contextmanager
def store_lock(store_path: Path, wait: bool = False):
    """Advisory file-level lock for a store directory.

    Acquires an exclusive lock on ``store_path / ".lock"``.
    When *wait* is ``False`` (default) the call fails fast with
    ``TimeoutError`` if the lock is held by another process.
    When *wait* is ``True`` it blocks until the lock is acquired.
    """
    lock_file = store_path / ".lock"
    lock_fd = os.open(lock_file, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        flags = fcntl.LOCK_EX
        if not wait:
            flags |= fcntl.LOCK_NB
        try:
            fcntl.lockf(lock_fd, flags)
        except BlockingIOError:
            raise SLDBStoreError(
                f"Store at {store_path} is busy (lock held by another process). "
                "Use --wait to block until the lock is available."
            )
        yield
        fcntl.lockf(lock_fd, fcntl.LOCK_UN)
    finally:
        os.close(lock_fd)


def _atomic_write(path: Path, content: str) -> None:
    """Write *content* to *path* atomically via a temp file and rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    try:
        os.write(fd, content.encode("utf-8"))
        os.fsync(fd)
        os.close(fd)
        fd = None
        os.replace(tmp_path, path)
    finally:
        if fd is not None:
            os.close(fd)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def load_store_index(store_path: Path) -> StoreIndex:
    index_file = store_path / "store_index.yaml"
    if not index_file.exists():
        raise FileNotFoundError(f"No store_index.yaml at {store_path}")
    data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
    return StoreIndex(**data)


def save_store_index(store_path: Path, index: StoreIndex) -> None:
    _atomic_write(
        store_path / "store_index.yaml",
        yaml.safe_dump(index.model_dump(), sort_keys=False),
    )


def load_models_index(path: Path) -> ModelsIndex:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return ModelsIndex(**data)


def save_models_index(path: Path, index: ModelsIndex) -> None:
    _atomic_write(
        path,
        yaml.safe_dump(index.model_dump(), sort_keys=False),
    )


def load_documents_index(path: Path) -> DocumentsIndex:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return DocumentsIndex(**data)


def save_documents_index(path: Path, index: DocumentsIndex) -> None:
    _atomic_write(
        path,
        yaml.safe_dump(index.model_dump(), sort_keys=False),
    )


def load_sections_index(path: Path) -> SectionsIndex:
    if not path.exists():
        return SectionsIndex()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return SectionsIndex(**data)


def save_sections_index(path: Path, index: SectionsIndex) -> None:
    _atomic_write(
        path,
        yaml.safe_dump(index.model_dump(), sort_keys=False),
    )


def load_semantic_dag(store_path: Path) -> SemanticDAG:
    dag_file = store_path / "semantic_dag.yaml"
    if not dag_file.exists():
        return SemanticDAG()
    data = yaml.safe_load(dag_file.read_text(encoding="utf-8")) or {}
    return SemanticDAG(**data)


def save_semantic_dag(store_path: Path, dag: SemanticDAG) -> None:
    _atomic_write(
        store_path / "semantic_dag.yaml",
        yaml.safe_dump(dag.model_dump(), sort_keys=False),
    )


def load_semantic_index(store_path: Path) -> SemanticIndex:
    index_file = store_path / "semantic_index.yaml"
    if not index_file.exists():
        return SemanticIndex()
    data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
    return SemanticIndex(**data)


def save_semantic_index(store_path: Path, index: SemanticIndex) -> None:
    _atomic_write(
        store_path / "semantic_index.yaml",
        yaml.safe_dump(index.model_dump(), sort_keys=False),
    )
