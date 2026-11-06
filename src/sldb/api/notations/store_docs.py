"""Every runtime document of a store, keyed by `Model:name`."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_docs(store: Path, pythonpath: str | None) -> dict[str, dict[str, Any]]:
    """`{"Model:name": {"model", "payload"}}` for the documents of the store."""
    import sldb.api as api

    return {
        f"{doc.model_name}:{doc.name}": {"model": str(doc.model_name), "payload": dict(doc.payload or {})}
        for doc in api.load_runtime_documents(Path(store), pythonpath, include_linked=False)
    }
