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
_LEGACY_CONTRACT = (
    "contract hash from before sldb signed class metadata (cecd97b): fields and template are "
    "the ones indexed, family/semantics/relations were never signed — `sldb stores update` "
    "re-seals it under the current formula"
)
_CONTRACT_MOVED = (
    "the model's contract (field schema or __template__) changed since it was indexed: "
    "extraction yields something else from the same text — `sldb stores update` re-extracts "
    "this model's documents"
)


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
    contract_ok: bool = True
    legacy_contract: bool = False   # contract_ok, but signed under the pre-cecd97b formula
    resolved: bool = True   # False when the class cannot be imported: fields were not re-extracted
    source_path: str = ""   # the .py the contract is declared in: what to open when it moved
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

    def inspect(self) -> str:
        """What the operator should open to judge this model's finding."""
        if not self.contract_ok:
            return self.source_path or f"the class registered as {self.name}"
        return f"{len(self.documents)} documents tracked under {self.name}"

    def explain(self) -> str:
        """One line on the model verdict, in terms of which child moved the node."""
        if not self.contract_ok:
            return _CONTRACT_MOVED
        if self.roster_ok:
            return _LEGACY_CONTRACT if self.legacy_contract else "ok"
        if not self.documents:
            return _EMPTY_ROSTER
        if self.roster_only_failure:
            return _ROSTER_ONLY.format(n=len(self.documents))
        return _ROSTER_AND_DOCS
