"""The pieces of a document/model verdict: which fields moved, which note the hashes earn, and
whether the model's contract still stands."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.field_set_drift import document_drifted
from sldb.store.model_node import contract_moved


def changed_fields(in_index: dict[str, str], on_disk: dict[str, str]) -> list[str]:
    """The field names whose hashes disagree, plus those present on only one side.

    Empty when either side has no map: a store written before `field_hashes` cannot be asked
    which field moved, and saying "none" there would read as "nothing changed" when
    `content_hash` already said otherwise.
    """
    if not in_index or not on_disk:
        return []
    return sorted(name for name in set(in_index) | set(on_disk) if in_index.get(name) != on_disk.get(name))


def note(content_ok: bool, fields_ok: bool, contract_ok: bool) -> DiagnosisNote:
    """Which verdict the two hashes earn — and who to blame when the fields disagree.

    Fields differing while the text stands still is not the document's doing when the model's
    contract moved: the same text extracts to something else now. Blaming the document there
    sent the reader to inspect a file nobody had edited.

    The contract only excuses the document while its TEXT is intact (`content_ok`). A moved
    contract on a file that was also edited is still a data mutation and still needs a human:
    letting the contract absolve it would hide a hand edit behind a safe-to-run verdict.
    """
    if content_ok and fields_ok:
        return DiagnosisNote.OK
    if fields_ok:
        return DiagnosisNote.BENIGN_MUTATION
    return DiagnosisNote.CONTRACT_MUTATION if not contract_ok and content_ok else DiagnosisNote.DATA_MUTATION


def contract_ok(models_idx, docs_idx, root: Path, model_type: Any, legacy: bool) -> bool:
    """The model's contract has not moved and no document's field set drifted (sldb.store.field_set_drift)."""
    drifted = any(document_drifted(d, root, model_type) for d in docs_idx.documents)
    return (legacy or not contract_moved(models_idx, model_type)) and not drifted
