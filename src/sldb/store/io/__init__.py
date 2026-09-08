from pathlib import Path
from sldb.store.io.lock import StoreIOLock
from sldb.store.io.store_index import StoreIndexIO
from sldb.store.io.models_index import ModelsIndexIO
from sldb.store.io.documents_index import DocumentsIndexIO
from sldb.store.io.sections_index import SectionsIndexIO
from sldb.store.io.semantic_dag import SemanticDAGIO
from sldb.store.io.semantic_index import SemanticIndexIO
from sldb.store.models import DocumentsIndex, ModelsIndex, SectionsIndex, SemanticDAG, SemanticIndex, StoreIndex

def store_lock(store_path: Path, wait: bool = False):
    return StoreIOLock(store_path).acquire(wait)

# -- index cache ---------------------------------------------------------------------------
#
# The three yaml indexes are read by every query and every operation, many times per call
# chain. Each parsed index is kept keyed by its file's path, mtime and size, and returned as
# a deep copy so a caller that mutates and saves it never changes the cached object; the save
# changes the file, and the next load sees a new signature.

from sldb.store.layout import semantic_dag_path as _semantic_dag_path, semantic_index_path as _semantic_index_path, store_index_path as _store_index_path

_INDEXES: dict[str, tuple[tuple, object]] = {}


def _file_signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


def _cached(path: Path, loader):
    key = str(path)
    sig = _file_signature(path)
    hit = _INDEXES.get(key)
    if hit is None or hit[0] != sig:
        hit = (sig, loader())
        _INDEXES[key] = hit
    return hit[1].model_copy(deep=True)


def invalidate_index_cache() -> None:
    _INDEXES.clear()
    _SAVED.clear()


_SAVED: dict[str, tuple[tuple, str]] = {}   # path -> (file signature, digest of what was last saved there)


def _digest(index) -> str:
    import hashlib
    import json
    return hashlib.sha256(json.dumps(index.model_dump(), sort_keys=True, default=str).encode()).hexdigest()


def _save_if_changed(path: Path, index, saver) -> None:
    """Write only when the content differs from what the file already holds: a rebuild that
    changes nothing leaves the file, its mtime and every cache keyed on it alone."""
    digest = _digest(index)
    prior = _SAVED.get(str(path))
    if prior is not None and prior[1] == digest and prior[0] == _file_signature(path):
        return
    saver()
    _SAVED[str(path)] = (_file_signature(path), digest)
    _INDEXES[str(path)] = (_file_signature(path), index.model_copy(deep=True))


def load_store_index(store_path: Path) -> StoreIndex:
    return _cached(_store_index_path(store_path), lambda: StoreIndexIO.load(store_path))

def save_store_index(store_path: Path, index: StoreIndex) -> None:
    _save_if_changed(_store_index_path(store_path), index, lambda: StoreIndexIO.save(store_path, index))

def load_models_index(path: Path) -> ModelsIndex:
    return _cached(path, lambda: ModelsIndexIO.load(path))

def save_models_index(path: Path, index: ModelsIndex) -> None:
    _save_if_changed(path, index, lambda: ModelsIndexIO.save(path, index))

def load_documents_index(path: Path) -> DocumentsIndex:
    return _cached(path, lambda: DocumentsIndexIO.load(path))

def save_documents_index(path: Path, index: DocumentsIndex) -> None:
    _save_if_changed(path, index, lambda: DocumentsIndexIO.save(path, index))

def load_sections_index(path: Path) -> SectionsIndex:
    return _cached(path, lambda: SectionsIndexIO.load(path))

def save_sections_index(path: Path, index: SectionsIndex) -> None:
    _save_if_changed(path, index, lambda: SectionsIndexIO.save(path, index))

def load_semantic_dag(store_path: Path) -> SemanticDAG:
    return _cached(_semantic_dag_path(store_path), lambda: SemanticDAGIO.load(store_path))

def save_semantic_dag(store_path: Path, dag: SemanticDAG) -> None:
    _save_if_changed(_semantic_dag_path(store_path), dag, lambda: SemanticDAGIO.save(store_path, dag))

def load_semantic_index(store_path: Path) -> SemanticIndex:
    return _cached(_semantic_index_path(store_path), lambda: SemanticIndexIO.load(store_path))

def save_semantic_index(store_path: Path, index: SemanticIndex) -> None:
    _save_if_changed(_semantic_index_path(store_path), index, lambda: SemanticIndexIO.save(store_path, index))
