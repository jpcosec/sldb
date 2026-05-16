from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DiagnosisNote(str, Enum):
    """Enumeration of diagnostic outcomes for documents."""

    OK = "ok"
    BENIGN_MUTATION = "benign_mutation"
    DATA_MUTATION = "data_mutation"
    MISSING = "missing"


@dataclass
class DocumentDiagnosis:
    """Diagnostic state for a single document."""

    name: str
    path: str
    hash_c_ok: bool
    hash_d_ok: bool
    path_exists: bool
    note: DiagnosisNote


@dataclass
class ModelDiagnosis:
    """Diagnostic state for a model and its documents."""

    name: str
    hash_b_ok: bool
    documents: list[DocumentDiagnosis] = field(default_factory=list)


@dataclass
class StoreDiagnosis:
    """Full diagnostic state for the entire store."""

    hash_a_ok: bool
    models: list[ModelDiagnosis] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Returns True if the store is in a valid state."""
        bad = {DiagnosisNote.DATA_MUTATION, DiagnosisNote.MISSING}
        return (
            self.hash_a_ok
            and all(m.hash_b_ok for m in self.models)
            and all(d.note not in bad for m in self.models for d in m.documents)
        )
