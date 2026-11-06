"""The rows of a section: `select_documents` with `{param}` filled, each row with its projected fields."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from sldb.api.documents.select_documents import select_documents
from sldb.core.exceptions import SLDBValidationError

PLACEHOLDER = re.compile(r"\{([A-Za-z_]\w*)\}")
ROW_KEYS = ("export_id", "model", "name", "path")


def section_rows(store_path: Path, index: Any, section: Any, values: dict[str, str]) -> list[dict[str, Any]]:
    """`{export_id, model, name, path, fields}` per selected document, in selection order."""
    chosen = select_documents(store_path, substituted(section.select, values))
    return [row_of(index, found, section.fields) for found in chosen]


def substituted(select: dict[str, Any], values: dict[str, str]) -> dict[str, Any]:
    """The selector with every `{param}` filled: in `where` as a string literal of the
    predicate (where_subject's syntax; a value holding a quote cannot be written), elsewhere
    as the text itself."""
    filled = {}
    for key, value in select.items():
        filled[key] = PLACEHOLDER.sub(lambda m: _filled(values, m.group(1), key == "where"), value) if isinstance(value, str) else value
    return filled


def _filled(values: dict[str, str], name: str, quoted: bool) -> str:
    if name not in values:
        raise SLDBValidationError(f"param {name!r} has no value: give it or declare a default")
    if quoted and '"' in values[name]:
        raise SLDBValidationError(f"param {name!r} cannot hold a double quote: {values[name]!r}")
    return f'"{values[name]}"' if quoted else values[name]


def resolve_params(view: Any, given: dict[str, Any]) -> dict[str, str]:
    """The values the view runs with (q15): every given param declared and a string, every
    required one present, defaults filled; in declaration order."""
    declared = {param.name: param for param in view.params}
    check_params(view.name, declared, given)
    values = {name: given.get(name, param.default) for name, param in declared.items()}
    return {name: value for name, value in values.items() if value is not None}


def check_params(view: str, declared: dict[str, Any], given: dict[str, Any]) -> None:
    unknown = sorted(set(given) - set(declared))
    if unknown:
        raise SLDBValidationError(f"view {view!r} declares no params {unknown}")
    missing = sorted(name for name, param in declared.items() if param.required and name not in given)
    if missing:
        raise SLDBValidationError(f"view {view!r} requires params {missing}")
    not_text = sorted(name for name, value in given.items() if not isinstance(value, str))
    if not_text:
        raise SLDBValidationError(f"params must be strings: {not_text}")


def row_of(index: Any, found: dict[str, str], fields: list[str]) -> dict[str, Any]:
    """The row of one selected document, its `fields` read from the index's projection."""
    payload = projected(index, found["export_id"])
    chosen = dict(payload) if "*" in fields else {name: payload.get(name) for name in fields}
    return {**{key: found[key] for key in ROW_KEYS}, "fields": chosen}


def projected(index: Any, export_id: str) -> dict[str, Any]:
    """A document's projected payload as the index holds it; empty when the index lacks it."""
    node = index.node(export_id)
    return dict(node.payload) if node is not None else {}
