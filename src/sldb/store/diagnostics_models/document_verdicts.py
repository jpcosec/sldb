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
    DiagnosisNote.PATH_OUTSIDE_ROOT: (
        "the tracked path resolves outside the project root (a symlink, or a directory on the "
        "way, points elsewhere): sldb does not open it, and the edge index counts it as stale"
    ),
    DiagnosisNote.SYMLINK_NOT_READ: (
        "the tracked path is a symlink: sldb does not follow it, and the edge index counts it "
        "as stale"
    ),
    DiagnosisNote.DOC_INVALID: "its model rejects the text on disk: no field could be re-extracted",
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
    DiagnosisNote.PATH_OUTSIDE_ROOT: (
        "decide first: replace the symlink with the file itself inside the project, or sldb "
        "docs untrack <name>; nothing outside the root is read"
    ),
    DiagnosisNote.SYMLINK_NOT_READ: (
        "decide first: replace the symlink with the regular file it points to, or sldb docs "
        "untrack <name> and track the target"
    ),
    DiagnosisNote.DOC_INVALID: (
        "decide first: edit the file until its model accepts it (the first errors are named "
        "above), then sldb stores update; or sldb docs untrack <name> if it is gone on purpose"
    ),
}

# Verdicts a command must not paper over: a human decides before anything runs.
NEEDS_DECISION = (DiagnosisNote.DATA_MUTATION, DiagnosisNote.MISSING, DiagnosisNote.PATH_OUTSIDE_ROOT, DiagnosisNote.SYMLINK_NOT_READ, DiagnosisNote.DOC_INVALID)

# A data mutation over untouched text, under an unchanged contract: the file is what it was and
# so is the model; what reads it changed (an sldb upgrade that extracts more). `stores update`
# trusts unchanged text, so it never re-reads it; `models update` does.
REREAD_EXPLANATION = (
    "fields differ but neither the text on disk nor the model's contract moved: what extracts "
    "it changed (an sldb upgrade) — `sldb models update <Model>` re-extracts the model's documents"
)
REREAD_REMEDY = "safe to run: sldb models update <Model>   (stores update trusts text that did not move)"
