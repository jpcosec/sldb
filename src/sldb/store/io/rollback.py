"""Put files back as they were when a write raises halfway: a failed operation leaves no trace."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator


@contextmanager
def rollback_on_error(paths: list[Path], forget_caches: Callable[[], None]) -> Iterator[None]:
    """Snapshot `paths`; if the block raises, restore their bytes (or absence), call
    `forget_caches` so no in-memory copy outlives the restore, and re-raise."""
    saved = {path: path.read_bytes() if path.exists() else None for path in paths}
    try:
        yield
    except BaseException:
        for path, data in saved.items():
            _restore(path, data)
        forget_caches()
        raise


def _restore(path: Path, data: bytes | None) -> None:
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
