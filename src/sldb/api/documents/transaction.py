"""Several document writes undone together: `transaction(store)` opens a `Transaction` whose
operations write at once (what one writes, the next reads) and whose rollback, when the block
raises, puts every touched file back: the Markdown, the index entries and the derived shards.
`RollbackError` lives in `sldb.store.io.rollback` and is re-exported here (docs/architecture/transactions.md)."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from sldb.api.documents import transaction_ops as ops
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.transaction_state import TransactionState
from sldb.api.stores.open_store import open_store
from sldb.store.io.rollback import RollbackError

__all__ = ["RollbackError", "Transaction", "transaction"]

_OPEN: dict[str, TransactionState] = {}


@contextmanager
def transaction(store: str | Path | None = None, pythonpath: str | None = None) -> Iterator[Transaction]:
    """Open a transaction over a store; nested blocks over the same store join the open one.

    Every operation writes immediately and is visible to the next one. If the block raises,
    the outermost transaction restores every file its operations (and its nested blocks')
    touched, then forgets the in-memory caches; a nested block that raises defers to it.

    Args:
        store: The store (path, alias, or None to discover it), resolved with `open_store`.
        pythonpath: Directory to import the store's model modules from.

    Yields:
        The transaction's operations.

    Raises:
        RollbackError: When the rollback itself could not restore some file; chained to the
            exception that triggered it, with `unrestored` naming the files.
    """
    state = _join(open_store(store), pythonpath)
    try:
        yield Transaction(state)
    except BaseException as exc:
        _leave(state, exc)
        raise
    _leave(state, None)


def _join(location, pythonpath: str | None) -> TransactionState:
    key = str(location.store_path.resolve())
    state = _OPEN.get(key)
    if state is None:
        state = _OPEN[key] = TransactionState(location, pythonpath)
    state.depth += 1
    return state


def _leave(state: TransactionState, exc: BaseException | None) -> None:
    state.depth -= 1
    if state.depth:
        return
    _OPEN.pop(str(state.location.store_path.resolve()), None)
    if exc is not None:
        state.rollback(exc)


class Transaction:
    """The operations of one open transaction. Paths are relative to the project root (or
    absolute inside it); `ref` is a document name or its path as the store records it."""

    def __init__(self, state: TransactionState) -> None:
        self._state = state

    def create(self, model: str, name: str, payload: dict[str, Any], path: str | Path | None = None) -> DocumentReference:
        """`create_document`; without `path`, beside the model's documents (`<root>/<model>/` for its first)."""
        return ops.create(self._state, model, name, payload, path)

    def update(self, ref: str, payload: dict[str, Any], expected_source_hash: str | None = None, expected: Any = None) -> DocumentReference:
        """`save_document_payload`, guarded: `expected_source_hash` against the entry's source
        hash, then `expected` against the current payload; a failed guard is a `ConflictError`."""
        return ops.update(self._state, ref, payload, expected_source_hash, expected)

    def delete(self, ref: str) -> DocumentReference:
        """`delete_document`: untrack and remove the file."""
        return ops.delete(self._state, ref)

    def move(self, ref: str, new_path: str | Path) -> DocumentReference:
        """`move_document`: the file moves, the name stays, the edges are rebuilt."""
        return ops.move(self._state, ref, new_path)

    def track(self, path: str | Path, model: str, name: str | None = None) -> DocumentReference:
        """`track_document_file`; `name` defaults to the file stem."""
        return ops.track(self._state, path, model, name)

    def untrack(self, ref: str) -> DocumentReference:
        """`untrack_document`: the file stays."""
        return ops.untrack(self._state, ref)

    def write_file(self, path: str | Path, data: bytes, expected_sha256: str | None = None) -> Path:
        """Write a file the store does not model; `expected_sha256` guards its current bytes."""
        return ops.write_file(self._state, path, data, expected_sha256)

    def record(self, path: str | Path) -> Path:
        """Snapshot a file the caller writes on its own, so the rollback restores it too."""
        return ops.record(self._state, path)
