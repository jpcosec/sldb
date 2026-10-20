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
    def moved_contracts(self) -> list[ModelDiagnosis]:
        """Models whose class contract no longer matches the one the index recorded."""
        return [m for m in self.models if not m.contract_ok]

    @property
    def is_valid(self) -> bool:
        """Whether the diagnosis found no error: no tracked file gone, every model importable.

        A stale root or roster, a moved contract and a changed document are the source moving
        against the index: alerts, valid but to be looked at (`sldb.api.stores.store_findings`,
        docs/architecture/anchoring.md §4). What the store's surroundings break (links,
        structural noise) is judged by `stores check`, not here.
        """
        return all(m.resolved for m in self.models) and not any(d.note is DiagnosisNote.MISSING for _m, d in self.damaged_documents)

    @property
    def counts(self) -> list[str]:
        """The findings behind the verdict, as phrases; empty when all clean."""
        pairs = ((len(self.damaged_documents), "damaged"), (len(self.reformatted_documents), "reformatted (ok)"), (len(self.roster_only_models), "roster-only"), (len(self.moved_contracts), "contract moved"))
        return [f"{n} {label}" for n, label in pairs if n]

    def summary(self, ok: bool | None = None, tally: str = "") -> str:
        """One line: the verdict (`ok`, else `is_valid`), the counts behind it, and `tally`."""
        checked = sum(len(m.documents) for m in self.models)
        verdict = "PASS" if (self.is_valid if ok is None else ok) else "FAIL"
        tail = ([] if self.root_ok else ["root hash stale"]) + ([tally] if tally else [])
        return " — ".join([f"{verdict}: store integrity", f"{checked} documents in {len(self.models)} models", *self.counts, *tail])
