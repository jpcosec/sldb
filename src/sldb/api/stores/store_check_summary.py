"""The per-document projection of a store diagnosis for `check_store`: verdict by category and hash mismatches."""

from __future__ import annotations

from typing import Any


def _classified(diagnosis: Any) -> dict[str, Any]:
    """The verdict split by category.

    `mismatched` lists every hash that moved, including the expected ones (text moved,
    fields held still). `damaged` is the documents changed or gone.
    """
    return {
        "damaged": [{"doc": d.name, "model": m, "note": d.note.value, "explain": d.explain()} for m, d in diagnosis.damaged_documents],
        "reformatted": [d.name for _m, d in diagnosis.reformatted_documents],
        "roster_only": [m.name for m in diagnosis.roster_only_models],
        "moved_contracts": [m.name for m in diagnosis.moved_contracts],
    }


def _summarize(diagnosis: Any) -> dict[str, Any]:
    checked = 0
    mismatched: list[dict[str, Any]] = []
    for model in diagnosis.models:
        for doc in model.documents:
            checked += 1
            _collect_mismatches(doc, mismatched)
    return {"checked": checked, "mismatched": mismatched}


# (reported kind, ok flag, value on disk now, value the index recorded)
_KINDS = (
    ("hash_c", "content_ok", "content_on_disk", "content_in_index"),
    ("hash_d", "fields_ok", "fields_on_disk", "fields_in_index"),
)


def _collect_mismatches(doc: Any, mismatched: list[dict[str, Any]]) -> None:
    for kind, ok, expected, actual in _KINDS:
        if not getattr(doc, ok):
            mismatched.append({"doc": doc.name, "expected": getattr(doc, expected), "actual": getattr(doc, actual), "kind": kind})
