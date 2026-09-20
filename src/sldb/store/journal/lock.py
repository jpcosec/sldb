"""A dedicated advisory lock for journal appends, separate from the store index lock."""

from __future__ import annotations

import contextlib
import fcntl
import os
from pathlib import Path

from sldb.store.journal.layout import journal_lock_path


@contextlib.contextmanager
def journal_lock(store_path: Path):
    """Hold the journal lock while the caller appends, so the chain never interleaves."""
    lock_file = journal_lock_path(store_path)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_file, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX)
        yield
        fcntl.lockf(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)
