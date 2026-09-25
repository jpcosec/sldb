"""Store integrity check: the CLI's `sldb stores check` reached through sldb.api.

The verification itself is ``sldb.store.diagnostics.diagnose_store`` (the exact
function the CLI calls); this module only projects its per-document verdicts into
a compact ``{ok, checked, mismatched}`` summary with the expected/actual hashes
the diagnosis now carries. Nothing here re-checks the store.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def check_store(store_path: Path, project_root: Path, pythonpath: str | None = None) -> dict[str, Any]:
    """Run the CLI's store integrity check and summarize it."""
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.diagnostics import diagnose_store

    diagnosis = diagnose_store(store_path, resolve_model_ref, project_root, pythonpath=pythonpath)
    summary = _summarize(diagnosis)
    return {"ok": not summary["mismatched"], **_classified(diagnosis), **summary}


def _classified(diagnosis: Any) -> dict[str, Any]:
    """The verdict split by category.

    `mismatched` lists every hash that moved, including the expected ones (text moved,
    fields held still). `damaged` is the subset that actually invalidates the store,
    which is what `is_valid` reports.
    """
    return {
        "valid": diagnosis.is_valid,
        "damaged": [{"doc": d.name, "model": m, "note": d.note.value, "explain": d.explain()} for m, d in diagnosis.damaged_documents],
        "reformatted": [d.name for _m, d in diagnosis.reformatted_documents],
        "roster_only": [m.name for m in diagnosis.roster_only_models],
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