"""The human-readable rendering of a store diagnosis.

Written for an operator who has just been told something is wrong and has to decide what to
do. Every finding answers three questions in order: what moved, what to open to judge it, and
what to run. Two of the five categories are safe to fix with one command; two are decisions
where naming a command would be wrong, because the index holds the only record of the value
about to be overwritten. The report says which kind it is rather than leaving that to be
inferred from a hash.
"""

from __future__ import annotations
from typing import Any
from sldb.cli.commands.store_check_notes import print_notes
from sldb.store.diagnostics_models import DiagnosisNote


def print_report(res: Any) -> None:
    """The verdict, then every finding that produced it, then what to do."""
    print(res.summary())
    print_notes(res)
    if res.is_valid:
        return
    _print_root(res)
    for model in res.models:
        _print_model(model)
    _print_next_step(res)


def _print_root(res: Any) -> None:
    if not res.root_ok:
        print("\nstore_hash stale: a model node moved, or the set of models changed")
        print("    inspect : nothing on disk — the root is derived from the model nodes below")
        print("    fix     : safe to run: sldb stores update")


def _print_next_step(res: Any) -> None:
    """Close with the one thing to do next, not a glossary of every category."""
    blocked = [d for _m, d in res.damaged_documents if d.needs_decision]
    if blocked:
        print(f"\nnext: {len(blocked)} finding(s) need a decision before any command is run (see 'fix:' above).")
        return
    print("\nnext: sldb stores update   (every finding above is safe to reindex)")


def _print_model(model: Any) -> None:
    findings = [d for d in model.documents if d.note is not DiagnosisNote.OK]
    if model.roster_ok and model.contract_ok and not findings:
        return
    print(f"\n{model.name}: {len(model.documents)} documents")
    _print_model_finding(model)
    for doc in findings:
        _print_document(doc)


def _print_model_finding(model: Any) -> None:
    if model.contract_ok and model.roster_ok:
        return
    label = "contract moved" if not model.contract_ok else "roster stale"
    print(f"  {label}: {model.explain()}")
    print(f"    inspect : {model.inspect()}")
    if not model.contract_ok:
        print("    fix     : safe to run: sldb stores update")


def _print_document(doc: Any) -> None:
    print(f"  {doc.note.value}: {doc.name}")
    print(f"    what    : {doc.explain()}")
    print(f"    inspect : {doc.inspect()}")
    print(f"    fix     : {doc.remedy()}")
    _print_hash_pair("source_hash (text)  ", doc.content_on_disk, doc.content_in_index, doc.content_ok)
    _print_hash_pair("content_hash (fields)", doc.fields_on_disk, doc.fields_in_index, doc.fields_ok)


def _print_hash_pair(label: str, on_disk: str | None, in_index: str | None, ok: bool) -> None:
    """Both sides of a disagreement, labelled by where each was read. Evidence, listed last:
    it says a hash moved, which is what the lines above already explained in words."""
    if ok or on_disk is None and in_index is None:
        return
    print(f"    {label}: on disk {_short(on_disk)} != in index {_short(in_index)}")


def _short(value: str | None) -> str:
    return value[:12] if value else "(none)"
