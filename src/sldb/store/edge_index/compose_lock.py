"""Single flight for the composition of one edge index: concurrent callers of one key wait for
the first to compose instead of each composing (and holding) its own copy."""

from __future__ import annotations

import threading
from typing import Hashable

_GUARD = threading.Lock()
_LOCKS: dict[Hashable, threading.Lock] = {}


def compose_lock(key: Hashable) -> threading.Lock:
    """The lock of `key`, the same object for every caller in this process."""
    with _GUARD:
        return _LOCKS.setdefault(key, threading.Lock())
