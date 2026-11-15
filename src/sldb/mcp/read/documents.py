"""Documents of the store: one by reference, or many by selector."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.addresses import addressed_row, document_address, row_alias
from sldb.mcp.paging import page
from sldb.mcp.read.miss import missing

FIELD_ERRORS = (KeyError, IndexError, TypeError, ValueError)


def not_found(ref: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Why a reference names no single document: none, or several."""
    if rows:
        return {"found": False, "ref": ref, "explanation": f"{ref!r} names {len(rows)} documents; use one of their export ids", "candidates": [r["export_id"] for r in rows]}
    return missing("unknown_document", ref, {"found": False, "ref": ref, "explanation": f"the store tracks no document named {ref!r} (a linked store's document is written `alias:Model:name`)"})


def identity(document: dict[str, Any]) -> dict[str, Any]:
    """The fields of a serialized document that say what and where it is."""
    return {"model": document["model_name"], "name": document["id"], "path": document["path"], "version": document["version"], "semantic_tags": document["semantic_tags"], "provenance": document["provenance"]}


def document_head(store_path: Path, row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """The identity of a selected document, and its payload."""
    alias = row_alias(row)
    target = f"{row['model']}/{row['name']}" if alias is None else f"{alias}:{row['model']}/{row['name']}"
    document = api.serialize_document(api.runtime_document(store_path, None, target))
    head = {"found": True, "address": document_address(row["export_id"]), "export_id": row["export_id"], "store": alias or "local"}
    return {**head, **identity(document)}, document["payload"]


def field_of(head: dict[str, Any], payload: dict[str, Any], field: str) -> dict[str, Any]:
    """The value of one dotted field path, or why the document has none."""
    try:
        return {**head, "field": field, "value": api.deep_get(payload, field)}
    except FIELD_ERRORS as error:
        why = f"{head['export_id']} has no field {field!r} ({error}); its top-level fields are {sorted(payload)}"
        return missing("unknown_field", field, {**head, "found": False, "field": field, "explanation": why}, sorted(payload))


def read_document(store_path: Path, ref: str, field: str | None = None) -> dict[str, Any]:
    """A document by `[alias:]Model:name` (or name, `Model/name`, tracked path): its payload,
    or the value of one dotted `field` path."""
    rows = api.select_documents(store_path, {"ref": ref})
    if len(rows) != 1:
        return not_found(ref, rows)
    head, payload = document_head(store_path, rows[0])
    return {**head, "payload": payload} if field is None else field_of(head, payload, field)


def select_documents(store_path: Path, model: str | None, where: str | None, ref: str | None, prefix: str | None, path_glob: str | None, include_linked: bool, offset: int, limit: int) -> dict[str, Any]:
    """The documents a selector names (keys combined by conjunction; `where` is a predicate
    of SLDB's rules language over the payload projection)."""
    selector = {k: v for k, v in {"model": model, "where": where, "ref": ref, "prefix": prefix, "path_glob": path_glob}.items() if v}
    rows = [addressed_row(r) for r in api.select_documents(store_path, {**selector, "include_linked": include_linked})]
    if not rows and model and not api.is_model_registered(store_path, model):
        why = f"the store does not register a model named {model!r}; list_models names the ones it does (a linked store's model needs include_linked)"
        return missing("unknown_model", model, page([], offset, limit, why))
    return page(rows, offset, limit, None if rows else f"no document matches {selector or 'an empty selector'}")
