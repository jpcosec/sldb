"""`select_documents`: which tracked documents a selector names, as the library answers it.

The public face of `sldb.store.query_engine.document_selection`: it opens the store, splits
the `ref`'s link alias the way `doc_status` does, and turns `expect="one"` into the store's
errors (`SLDBDocumentTargetError` for none, `AmbiguousSelectionError` for several).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.selector import Selector
from sldb.api.edges.edge_reading import model_type_of
from sldb.api.stores.doc_ref import split_doc_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import AmbiguousSelectionError, SLDBDocumentTargetError
from sldb.store.query_engine.document_selection import select_rows

EXPECTATIONS = ("many", "one")


def select_documents(store: str | Path | None, selector: dict[str, Any] | Selector, *, expect: str = "many") -> list[dict[str, str]]:
    """The documents `selector` names, as `{export_id, model, name, path}` rows.

    Args:
        store: The store (path, alias, or None to discover it).
        selector: A `Selector` or its mapping: `ref`, `prefix`, `path_glob`, `model`, `where`
            and `include_linked`, combined by conjunction. Blank values and unknown keys are
            rejected (`pydantic.ValidationError`); an unparseable `where` raises
            `WherePredicateError`.
        expect: `"many"` returns every match (a prefix keeps every name starting with it);
            `"one"` returns exactly one row: by prefix, an exact name wins, else the one prefix
            match.

    Returns:
        Rows ordered by path, the local store's first and then each linked store's by alias.
        `export_id` is the document's node id in the edge index (`Model:name`, or
        `alias:Model:name` when it belongs to a linked store); `path` is relative to the
        project root of the store that tracks it.

    Raises:
        SLDBDocumentTargetError: `expect="one"` and nothing matched (`Unknown document: ...`).
        AmbiguousSelectionError: `expect="one"` and several matched; `candidates` names them.
        ValueError: `expect` is neither `"many"` nor `"one"`.
    """
    if expect not in EXPECTATIONS:
        raise ValueError(f"expect must be one of {EXPECTATIONS}, not {expect!r}")
    chosen = Selector.model_validate(selector)
    store_path = open_store(store, mode="readonly").store_path
    ref = None if chosen.ref is None else split_doc_ref(store_path, chosen.ref)
    keys = chosen.model_dump(exclude={"ref"})
    rows = select_rows(store_path, ref=ref, expect=expect, model_type_of=model_type_of, **keys)
    return rows if expect == "many" else _the_one(rows, chosen.describe())


def _the_one(rows: list[dict[str, str]], selector: str) -> list[dict[str, str]]:
    if len(rows) == 1:
        return rows
    if not rows:
        raise SLDBDocumentTargetError(f"Unknown document: {selector}")
    raise AmbiguousSelectionError(selector, [row["export_id"] for row in rows])
