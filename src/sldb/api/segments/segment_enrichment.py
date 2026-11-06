"""Enriches document segments with views, projections, and table data."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def enrich_segment(segment: dict[str, Any], store_path: Path | None, pythonpath: str | None) -> dict[str, Any]:
    """Enriches a segment dictionary with projection and table_data if applicable."""
    _enrich_projection(segment, store_path, pythonpath)
    _enrich_table(segment)
    return segment


def _enrich_projection(segment: dict[str, Any], store_path: Path | None, pythonpath: str | None) -> None:
    traits = segment.get("traits") or []
    comp = segment.get("composition") or {}
    ref_kind = comp.get("ref") if isinstance(comp, dict) else getattr(comp, "ref", None)
    if (any(t in ("diagram", "view") for t in traits) or ref_kind in ("view", "spec")) and store_path is not None:
        val = segment.get("value") or segment.get("ref") or segment.get("text")
        segment["projection"] = _resolve_projection(store_path, pythonpath, val)


def _enrich_table(segment: dict[str, Any]) -> None:
    traits = segment.get("traits") or []
    if any(t == "table" or t.startswith("table[") for t in traits):
        segment["table_data"] = _build_table_data(segment.get("value"), traits)


def _resolve_projection(store_path: Path, pythonpath: str | None, val: Any) -> dict[str, Any] | None:
    if not val or not isinstance(val, str):
        return None
    ref = val.strip().strip("`")
    if not (ref.startswith("SpecDoc:") or ref.startswith("ViewDoc:")):
        return None
    return _call_resolver(store_path, pythonpath, ref)


def _call_resolver(store_path: Path, pythonpath: str | None, ref: str) -> dict[str, Any]:
    try:
        from sldb.api.notations import evaluate_projection_view, resolve_view

        if ref.startswith("SpecDoc:"):
            return resolve_view(store_path, ref, pythonpath=pythonpath)
        return evaluate_projection_view(store_path, ref, pythonpath=pythonpath)
    except Exception as exc:
        return {"error": str(exc)}


def _build_table_data(value: Any, traits: list[str]) -> dict[str, Any]:
    cols = _extract_cols(traits, value)
    if not isinstance(value, list):
        return {"columns": cols, "rows": []}
    rows = []
    for item in value:
        d = item.model_dump(mode="json") if hasattr(item, "model_dump") else (dict(item) if isinstance(item, dict) else item)
        rows.append(d if isinstance(d, dict) else {cols[0]: d} if cols else {"value": d})
    return {"columns": cols, "rows": rows}


def _extract_cols(traits: list[str], value: Any) -> list[str]:
    for t in traits:
        if t.startswith("table[") and t.endswith("]"):
            return [c.strip() for c in t[6:-1].split(",") if c.strip()]
    if isinstance(value, list) and value:
        first = value[0]
        d = first.model_dump(mode="json") if hasattr(first, "model_dump") else (dict(first) if isinstance(first, dict) else None)
        if isinstance(d, dict):
            return list(d.keys())
    return []
