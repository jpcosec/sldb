"""What each document verdict means and what resolves it.

Kept beside the categories rather than inside a branch. Two of these are safe to fix with one
command; two are decisions, and naming a command there would be wrong — the index holds the
only record of the value a reindex would overwrite, and nothing else holds the previous one.
"""

from __future__ import annotations

from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote

EXPLANATIONS = {
    DiagnosisNote.OK: "ok",
    DiagnosisNote.BENIGN_MUTATION: (
        "text changed, fields identical (expected mutation: reformatting or marker "
        "churn) — `stores update` refreshes the index"
    ),
    DiagnosisNote.DATA_MUTATION: (
        "fields changed under the model's contract (a real data change) — `stores "
        "update` accepts it, but confirm the change was intended first"
    ),
    DiagnosisNote.CONTRACT_MUTATION: (
        "fields differ because the MODEL's contract moved, not the document: the text on "
        "disk is unchanged — `stores update` re-extracts it under the new contract"
    ),
}

REMEDIES = {
    DiagnosisNote.OK: "nothing to do",
    DiagnosisNote.BENIGN_MUTATION: "safe to run: sldb stores update",
    DiagnosisNote.CONTRACT_MUTATION: "safe to run: sldb stores update",
    DiagnosisNote.DATA_MUTATION: (
        "decide first: if the edit was intended, sldb stores update; if not, restore the file "
        "(git checkout -- <path>) before updating, because the index holds the previous hash "
        "and nothing else holds the previous value"
    ),
    DiagnosisNote.MISSING: (
        "decide first: restore the file if it was moved by accident, or sldb docs untrack "
        "<name> if it is gone on purpose"
    ),
}

# Verdicts a command must not paper over: a human decides before anything runs.
NEEDS_DECISION = (DiagnosisNote.DATA_MUTATION, DiagnosisNote.MISSING)
