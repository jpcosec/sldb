"""`sldb docs select`: CLI adapter over `sldb.api.select_documents`.

The flags are the selector's keys (`--ref`, `--prefix`, `--path-glob`, `--model`, `--where`,
`--include-linked`); `--one` is `expect="one"`. The JSON payload is the one `GET /docs/select`
answers with, so a caller reads both the same way.
"""
from __future__ import annotations
from typing import Any
from sldb.api.documents.select_documents import select_documents
from sldb.cli.output_format import emit

KEYS = ("ref", "prefix", "path_glob", "model", "where")


def docs_select(args: Any) -> int:
    selector, expect = selector_of(vars(args)), "one" if args.one else "many"
    rows = select_documents(args.store, selector, expect=expect)
    emit(selection_payload(selector, expect, rows), args.format, _text(rows))
    return 0


def selector_of(params: dict[str, Any]) -> dict[str, Any]:
    """The selector mapping the given keys make; `include_linked` only when set."""
    selector = {key: params[key] for key in KEYS if params.get(key) is not None}
    if params.get("include_linked"):
        selector["include_linked"] = True
    return selector


def selection_payload(selector: dict[str, Any], expect: str, rows: list[dict[str, str]]) -> dict[str, Any]:
    """The JSON of a selection: what was asked, how many were expected, and the rows."""
    return {"selector": selector, "expect": expect, "documents": rows}


def _text(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "No documents match"
    return "\n".join(f"{row['export_id']} -> {row['path']}" for row in rows)
