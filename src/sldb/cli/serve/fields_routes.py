"""GET /fields: a document's fields, addressable by dotted path and list index.

`/fields?doc=<id>` lists every top-level field with its model metadata plus the
leaf addresses of the payload (``leaf_paths``). Adding `path=<dotted>` narrows to
one value via ``sldb.api.deep_get`` — the same addressing `fields show
docs/<doc>/<path>` uses — and `index=<n>` steps into a list element. Unknown doc
or path -> 404; the editor never sees a traceback.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import deep_get, describe_field, leaf_paths, runtime_document
from sldb.cli.serve.params import query_params, require_param

_LIST_KINDS = {"list", "stringlist", "enumlist"}


def dispatch_fields(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    doc, error = require_param(query_params(handler), "doc")
    if error is not None:
        return error, 400
    runtime, error = _find(store_path, pythonpath, doc)
    if error is not None:
        return error, 404
    target = _target_path(query_params(handler))
    return _fields_for(runtime, target)


def _find(store_path: Path, pythonpath: str, doc: str) -> tuple[Any, dict[str, Any] | None]:
    try:
        return runtime_document(store_path, pythonpath, doc), None
    except ValueError as exc:
        return None, {"ok": False, "error": str(exc)}


def _fields_for(runtime: Any, target: str | None) -> tuple[dict[str, Any], int]:
    if target is None:
        return _all(runtime)
    return _one(runtime, target)


def _target_path(params: dict[str, str]) -> str | None:
    path = params.get("path")
    if path is None:
        return None
    index = params.get("index")
    return path if index is None else f"{path}.{index}"


def _all(runtime: Any) -> tuple[dict[str, Any], int]:
    references = _references(runtime)
    fields = [{"name": name, **_field_meta(name, field, runtime.payload, references)} for name, field in runtime.model_type.model_fields.items()]
    return {"doc": runtime.name, "model": runtime.model_name, "fields": fields, "leaf_paths": leaf_paths(runtime.payload)}, 200


def _field_meta(name: str, field: Any, payload: dict[str, Any], references: list[str]) -> dict[str, Any]:
    description = describe_field(name, field)
    return {
        "value": payload.get(name),
        "type": description.annotation,
        "is_list": description.kind in _LIST_KINDS,
        "is_required": description.required,
        "is_reference": name in references,
        "description": description.description,
    }


def _one(runtime: Any, path: str) -> tuple[dict[str, Any], int]:
    try:
        value = deep_get(runtime.payload, path)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        return {"ok": False, "error": f"Unknown field path '{path}': {exc}"}, 404
    top = path.split(".", 1)[0]
    if top not in runtime.model_type.model_fields:
        return {"doc": runtime.name, "model": runtime.model_name, "path": path, "value": value, "type": _value_type(value), "is_list": isinstance(value, list)}, 200
    return {"doc": runtime.name, "model": runtime.model_name, "path": path, "value": value, **_meta(runtime, top)}, 200


def _meta(runtime: Any, top: str) -> dict[str, Any]:
    description = describe_field(top, runtime.model_type.model_fields[top])
    return {
        "type": description.annotation,
        "is_list": description.kind in _LIST_KINDS,
        "is_required": description.required,
        "is_reference": top in _references(runtime),
    }


def _references(runtime: Any) -> list[str]:
    return list(getattr(runtime.model_type, "__references__", []) or [])


def _value_type(value: Any) -> str:
    return type(value).__name__