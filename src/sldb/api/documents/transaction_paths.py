"""Which files a document write may move, so a transaction snapshots them before the write;
where a new document goes by default; and the cheap signature walk that catches a file the
transaction moved without a snapshot."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_declaration import declaration_path
from sldb.core.exceptions import SLDBStoreError
from sldb.store import documents_hash
from sldb.store.layout import cache_dir, documents_shard_path, edges_model_shard_path, edges_shard_path, edges_store_shard_path, lock_path, models_index_relpath, sections_shard_path, semantic_dag_path, semantic_index_path, semantic_shard_path, store_index_path


def document_files(sp: Path, root: Path, model: str, name: str, doc_path: Path | None) -> list[Path]:
    """The document's Markdown, its index shard, its derived shards and the files every write
    under `model` may rewrite."""
    own = [documents_shard_path(sp, model, name), semantic_shard_path(sp, model, name), sections_shard_path(sp, model, name), edges_shard_path(sp, model, name)]
    return ([doc_path] if doc_path is not None else []) + own + model_files(sp, root, model)


def model_files(sp: Path, root: Path, model: str) -> list[Path]:
    """The model's index and edges shard, the store index, the store-wide derived files and
    the declaration: what any write of a `model` document may move besides its own shards."""
    return [root / models_index_relpath(sp, model), edges_model_shard_path(sp, model), store_index_path(sp), edges_store_shard_path(sp), semantic_dag_path(sp), semantic_index_path(sp), declaration_path(sp)]


def inside(root: Path, raw: str | Path) -> Path:
    """`raw` resolved against the project root (an absolute path as is); outside it, refused."""
    path = Path(raw)
    resolved = (path if path.is_absolute() else root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise SLDBStoreError(f"Path '{raw}' is outside the project root {root}.")
    return resolved


def default_document_path(sp: Path, root: Path, model: str, name: str) -> Path:
    """Beside the model's first tracked document, or under `<root>/<model>/` when it has none."""
    entries = documents_hash.entries_of(sp, model)
    directory = root / Path(entries[0].path).parent if entries else root / model
    return directory / f"{name}.md"


def store_signatures(sp: Path) -> dict[Path, tuple[int, int]]:
    """(mtime, size) of every file of the store and of its cache, lock files aside."""
    locks = lock_path(sp).parent
    found = {}
    for base in (sp, cache_dir(sp)):
        for path in base.rglob("*") if base.is_dir() else []:
            if path.is_file() and locks not in path.parents:
                found[path] = _signature(path)
    return found


def _signature(path: Path) -> tuple[int, int]:
    st = path.stat()
    return (st.st_mtime_ns, st.st_size)


def unsnapshotted_drift(before: dict[Path, tuple[int, int]], sp: Path, saved: dict[Path, bytes | None]) -> tuple[list[Path], list[Path]]:
    """Files that moved without a snapshot since `before`: the new ones (safe to delete) and
    the changed or missing ones (nothing to restore them from)."""
    after = store_signatures(sp)
    new = [path for path in after if path not in before and path not in saved]
    changed = [path for path, sig in before.items() if path not in saved and after.get(path) != sig]
    return new, changed
