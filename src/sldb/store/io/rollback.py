"""Put files back as they were when a write raises halfway: a failed operation leaves no trace.

`rollback_on_error` covers one operation's files. `snapshot` and `restore_all` are the same
mechanism spread over a whole transaction (`sldb.api.transaction`): the first snapshot of a
path is the state a rollback goes back to, however many writes touch it afterwards."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterable, Iterator

from sldb.store.exceptions import SLDBStoreError


class RollbackError(SLDBStoreError):
    """A rollback could not put every file back. `unrestored` lists the ones still not as they
    were: paths relative to the project root, in the order their restore was tried. The
    exception that triggered the rollback is `__cause__`."""

    def __init__(self, unrestored: list[str]) -> None:
        super().__init__(f"Rollback incomplete; not restored: {', '.join(unrestored)}")
        self.unrestored = unrestored


@contextmanager
def rollback_on_error(paths: list[Path], forget_caches: Callable[[], None]) -> Iterator[None]:
    """Snapshot `paths`; if the block raises, restore their bytes (or absence), call
    `forget_caches` so no in-memory copy outlives the restore, and re-raise."""
    saved: dict[Path, bytes | None] = {}
    snapshot(paths, saved)
    try:
        yield
    except BaseException:
        restore_all(saved)
        forget_caches()
        raise


def snapshot(paths: Iterable[Path], saved: dict[Path, bytes | None]) -> None:
    """Remember the bytes (or the absence) of each path `saved` does not know yet."""
    for path in paths:
        if path not in saved:
            saved[path] = path.read_bytes() if path.exists() else None


def restore_all(saved: dict[Path, bytes | None]) -> list[Path]:
    """Put every path back, in snapshot order. A path whose restore raises does not stop the
    others; it is returned."""
    failed = []
    for path, data in saved.items():
        try:
            _restore(path, data)
        except Exception:
            failed.append(path)
    return failed


def _restore(path: Path, data: bytes | None) -> None:
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
