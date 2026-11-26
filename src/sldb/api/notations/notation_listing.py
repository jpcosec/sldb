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


def _standard_of(raw: Any) -> dict[str, Any] | None:
    if isinstance(raw, dict) and isinstance(raw.get("name"), str) and raw["name"].strip():
        return {"name": raw["name"], "version": raw.get("version")}
    return None


def _builtin_standard(name: str) -> dict[str, Any] | None:
    from sldb.notations.notation_files import load_notation

    try:
        std = load_notation(name).standard
    except Exception:
        return None
    return std.model_dump() if std else None


def _builtin_standards() -> dict[str, dict[str, Any]]:
    found = {name: _builtin_standard(name) for name in sorted(builtin_notations())}
    return {name: std for name, std in found.items() if std}


def _doc_standard(d: Any) -> dict[str, Any] | None:
    if d.model_name != "NotationDoc":
        return None
    return _standard_of(getattr(d.payload, "get", lambda *_: None)("standard"))


def _store_standards(store: Path | str, pythonpath: str | None) -> dict[str, dict[str, Any]]:
    try:
        import sldb.api as api

        docs = api.load_runtime_documents(Path(store), pythonpath, include_linked=False)
        found = {f"NotationDoc:{d.name}": _doc_standard(d) for d in docs}
    except Exception:
        return {}
    return {ref: std for ref, std in found.items() if std}


def notation_standards(store: Path | str, pythonpath: str | None) -> dict[str, dict[str, Any]]:
    """`{<notation ref or builtin name>: {name, version}}` for the notations that declare a standard."""
    return {**_builtin_standards(), **_store_standards(store, pythonpath)}


def list_notations(store: Path | str, pythonpath: str | None) -> dict[str, Any]:
    """`{builtin_notations, builtin_palettes, store_notations}`, plus `standards` when a notation declares one."""
    out: dict[str, Any] = {
        "builtin_notations": sorted(builtin_notations()),
        "builtin_palettes": sorted(builtin_palettes()),
        "store_notations": store_notation_refs(store, pythonpath),
    }
    standards = notation_standards(store, pythonpath)
    if standards:
        out["standards"] = standards
    return out
