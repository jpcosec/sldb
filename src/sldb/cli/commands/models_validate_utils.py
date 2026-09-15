from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Any, Iterator
from sldb.cli.store_context import get_store_context
from sldb.store.layout import core_dir, semantic_dag_path, semantic_index_path
from sldb.core.exceptions import SLDBModelEditError
from sldb.runtime.validation import Validator

def validate_template_contract(model_type: Any) -> None:
    recipes = Validator(model_type)._get_recipes()
    field_names = set(model_type.model_fields)
    referenced = _extract_referenced_fields(recipes)
    unknown = sorted(name for name in referenced if name not in field_names)
    if unknown:
        raise SLDBModelEditError(f"Draft for '{model_type.__name__}' references unknown fields: {', '.join(unknown)}")

def _extract_referenced_fields(recipes: list[Any]) -> set[str]:
    referenced: set[str] = set()
    for recipe in recipes:
        markers = list(recipe.get("props_info", []))
        if "marker" in recipe:
            markers.append(recipe["marker"])
        if "col_markers" in recipe:
            for marker_info in recipe["col_markers"].values():
                markers.append(marker_info["marker"])
        _add_marker_names(markers, referenced)
    return referenced

def _add_marker_names(markers: list[Any], referenced: set[str]) -> None:
    for marker in markers:
        name = getattr(marker, "name", None)
        if isinstance(marker, dict):
            name = marker.get("name")
        if name:
            referenced.add(name)

def store_index_files(store: Any) -> list[Path]:
    """Every file a model reindex may rewrite: the store core indexes and the semantic runtime indexes."""
    sp, _root = get_store_context(store)
    return [*(p for p in core_dir(sp).rglob("*") if p.is_file()), semantic_index_path(sp), semantic_dag_path(sp)]

@contextlib.contextmanager
def restored_on_failure(paths: list[Path]) -> Iterator[None]:
    """Snapshot ``paths``; if the block raises, write them back and re-raise."""
    snapshot = {p: p.read_bytes() if p.exists() else None for p in paths}
    try:
        yield
    except BaseException:
        _restore(snapshot)
        raise

def _restore(snapshot: dict[Path, bytes | None]) -> None:
    for p, content in snapshot.items():
        if content is None:
            p.unlink(missing_ok=True)
        else:
            p.write_bytes(content)
