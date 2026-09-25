"""The human-readable rendering of a store diagnosis.

A single PASS/FAIL line cannot distinguish a store that was merely reformatted from
one whose data changed from one whose document list is incomplete. All three used to
print identically; each now prints its own reason, the documents involved, and the
command that resolves it.
"""

from __future__ import annotations
from typing import Any
from sldb.store.diagnostics_models import DiagnosisNote

_ROOT_STALE = (
    "\nroot hash (hash_a) disagrees: the set of models or their roster hashes moved",
    "  fix: sldb stores update",
)

_LEGEND = (
    "\nwhat the categories mean:",
    "  benign_mutation  text moved, fields identical — expected, does not fail the store",
    "  data_mutation    a field's value changed under the model's contract",
    "  missing          tracked in the index, absent from disk",
    "  roster-only      the list disagrees although every document present is clean",
)


def print_report(res: Any) -> None:
    """The verdict, then every finding that produced it, naming names."""
    print(res.summary())
    if not res.root_ok:
        print("\n".join(_ROOT_STALE))
    for model in res.models:
        _print_model(model)
    if not res.is_valid:
        print("\n".join(_LEGEND))


def _print_model(model: Any) -> None:
    findings = [d for d in model.documents if d.note is not DiagnosisNote.OK]
    if model.roster_ok and not findings:
        return
    print(f"\n{model.name}: {len(model.documents)} documents")
    if not model.roster_ok:
        print(f"  roster (hash_b): {model.explain()}")
    for doc in findings:
        _print_document(doc)


def _print_document(doc: Any) -> None:
    print(f"  {doc.note.value}: {doc.name}")
    print(f"    path    : {doc.path}")
    print(f"    {doc.explain()}")
    _print_hash_pair("content (hash_c)", doc.content_on_disk, doc.content_in_index, doc.content_ok)
    _print_hash_pair("fields  (hash_d)", doc.fields_on_disk, doc.fields_in_index, doc.fields_ok)


def _print_hash_pair(label: str, on_disk: str | None, in_index: str | None, ok: bool) -> None:
    """Both sides of a disagreement, labelled by where each was read."""
    if ok or on_disk is None and in_index is None:
        return
    print(f"    {label}: on disk {_short(on_disk)} != in index {_short(in_index)}")


def _short(value: str | None) -> str:
    return value[:12] if value else "(none)"
