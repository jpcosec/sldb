from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from sldb.store.diagnostics_models.diagnosis_note import DiagnosisNote


@dataclass
class DocumentDiagnosis:
    """Diagnostic state for a single document."""

    name: str
    path: str
    hash_c_ok: bool
    hash_d_ok: bool
    path_exists: bool
    note: DiagnosisNote
    hash_c_expected: str | None = None
    hash_c_actual: str | None = None
    hash_d_expected: str | None = None
    hash_d_actual: str | None = None
