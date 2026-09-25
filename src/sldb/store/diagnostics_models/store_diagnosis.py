from __future__ import annotations
from dataclasses import dataclass, field
from sldb.store.diagnostics_models.model_diagnosis import ModelDiagnosis
from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote

_DAMAGING = (DiagnosisNote.DATA_MUTATION, DiagnosisNote.MISSING)


@dataclass
class StoreDiagnosis:
    """Full diagnostic state for the entire store.

    ``root_ok`` is `hash_a`: the store index signs `[{name, hash_b}]` over every
    registered model, so it is the Merkle root of the whole store.
    """

    root_ok: bool
    models: list[ModelDiagnosis] = field(default_factory=list)

    @property
    def hash_a_ok(self) -> bool:
        """Deprecated alias for `root_ok`."""
        return self.root_ok

    @property
    def damaged_documents(self) -> list[tuple[str, object]]:
        """(model, diagnosis) per document that is damaged, not merely reformatted."""
        return [(m.name, d) for m in self.models for d in m.documents if d.note in _DAMAGING]

    @property
    def reformatted_documents(self) -> list[tuple[str, object]]:
        """(model, diagnosis) per document whose text moved but whose fields held still."""
        return [(m.name, d) for m in self.models for d in m.documents if d.note is DiagnosisNote.BENIGN_MUTATION]

    @property
    def roster_only_models(self) -> list[ModelDiagnosis]:
        """Models whose roster hash disagrees although no document present is damaged."""
        return [m for m in self.models if m.roster_only_failure]

    @property
    def is_valid(self) -> bool:
        """Whether the store is in a valid state.

        Verdict unchanged by the rename: a reformatted document (text moved, fields
        identical) is still valid, a damaged one is not, and a disagreeing roster or
        root hash is not. `roster_only_models` explains such a failure without
        excusing it — classifying a failure is not the same as tolerating it.
        """
        return self.root_ok and all(m.roster_ok for m in self.models) and not self.damaged_documents

    @property
    def counts(self) -> list[str]:
        """The findings behind the verdict, as phrases; empty when all clean."""
        pairs = ((len(self.damaged_documents), "damaged"), (len(self.reformatted_documents), "reformatted (ok)"), (len(self.roster_only_models), "roster-only"))
        return [f"{n} {label}" for n, label in pairs if n]

    def summary(self) -> str:
        """One line: the verdict and the counts behind it."""
        checked = sum(len(m.documents) for m in self.models)
        head = ["PASS" if self.is_valid else "FAIL", f"{checked} documents in {len(self.models)} models"]
        tail = [] if self.root_ok else ["root hash stale"]
        return " — ".join([f"{head[0]}: store integrity", head[1], *self.counts, *tail])
