"""The notations and palettes available: builtins plus the NotationDocs in a store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.notations.notation import builtin_notations
from sldb.notations.palette import builtin_palettes


def store_notation_refs(store: Path | str, pythonpath: str | None) -> list[str]:
    """`NotationDoc:<name>` of the notations in the store; empty if it cannot be read."""
    try:
        import sldb.api as api

        docs = api.load_runtime_documents(Path(store), pythonpath, include_linked=False)
        return [f"NotationDoc:{d.name}" for d in docs if d.model_name == "NotationDoc"]
    except Exception:
        return []


def list_notations(store: Path | str, pythonpath: str | None) -> dict[str, Any]:
    """`{builtin_notations, builtin_palettes, store_notations}`."""
    return {
        "builtin_notations": sorted(builtin_notations()),
        "builtin_palettes": sorted(builtin_palettes()),
        "store_notations": store_notation_refs(store, pythonpath),
    }
