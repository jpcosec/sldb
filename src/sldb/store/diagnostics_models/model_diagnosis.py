from __future__ import annotations
from dataclasses import dataclass, field
from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote
from sldb.store.diagnostics_models.document_diagnosis import DocumentDiagnosis

_CLEAN = (DiagnosisNote.OK, DiagnosisNote.BENIGN_MUTATION)

_EMPTY_ROSTER = (
    "roster hash disagrees over 0 documents on disk: the index counts documents this "
    "tree does not contain (an unversioned family?), so nothing can be summed — no "
    "document is damaged"
)
_ROSTER_ONLY = (
    "roster hash disagrees but all {n} documents present are clean: the list is "
    "incomplete or a document joined/left without reindexing — `stores update` "
    "recomputes it"
)
_ROSTER_AND_DOCS = "roster hash disagrees, and documents below are damaged too"


@dataclass
class ModelDiagnosis:
    """Diagnostic state for a model and its documents.

    ``roster_ok`` is `hash_b`: the model's index signs `[{name, hash_c, hash_d}]`
    over its whole document list, so it moves when any document is written AND when
    a document joins or leaves the roster. It is a statement about the LIST, which is
    why it can fail while every document present is individually fine.
    """

    name: str
    roster_ok: bool
    documents: list[DocumentDiagnosis] = field(default_factory=list)

    @property
    def hash_b_ok(self) -> bool:
        """Deprecated alias for `roster_ok`."""
        return self.roster_ok

    @property
    def documents_are_clean(self) -> bool:
        """Whether every document present is individually fine."""
        return all(d.note in _CLEAN for d in self.documents)

    @property
    def roster_only_failure(self) -> bool:
        """The roster hash disagrees, yet no document present is damaged.

        The signature of a document list that is INCOMPLETE rather than corrupt: the
        documents the index signed are not all here to be summed. Common cause is a
        deliberately unversioned family (a ledger whose documents are gitignored),
        where a clean clone has an index counting documents it was never meant to
        contain. Nothing is damaged, and no per-document verdict can show it because
        the absent documents have no verdict at all.
        """
        return not self.roster_ok and self.documents_are_clean

    def explain(self) -> str:
        """One line on the roster verdict, in terms of what it implies."""
        if self.roster_ok:
            return "ok"
        if not self.documents:
            return _EMPTY_ROSTER
        if self.roster_only_failure:
            return _ROSTER_ONLY.format(n=len(self.documents))
        return _ROSTER_AND_DOCS
