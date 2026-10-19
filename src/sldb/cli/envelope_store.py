"""The `store` and `revision` of an envelope: the store the command ran against, if any."""

from __future__ import annotations

import contextlib
import io
from typing import Any

from sldb.api.stores.open_store import open_store
from sldb.store.io import load_store_index


def envelope_store(argv: list[str]) -> dict[str, Any]:
    """`{"store": {"path"}, "revision": store_hash}`, or both null when no store resolves."""
    arg = _store_arg(argv)
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            location = open_store(arg)
            revision = load_store_index(location.store_path).store_hash or None
    except Exception:  # noqa: BLE001 - a command without a store still gets an envelope
        return {"store": None, "revision": None}
    return {"store": {"path": str(location.store_path)}, "revision": revision}


def _store_arg(argv: list[str]) -> str | None:
    return argv[argv.index("--store") + 1] if "--store" in argv[:-1] else None
