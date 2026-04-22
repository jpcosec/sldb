import dataclasses
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Type

from sldb.store.models import ModelsIndex
from sldb.store.io import load_store_index, load_models_index, load_documents_index
from sldb.store.hashing import hash_text, hash_fields, hash_documents_index, hash_models_layer
from sldb.structuredNLDoc import StructuredNLDoc


class DiagnosisNote(str, Enum):
    OK = "ok"
    BENIGN_MUTATION = "benign_mutation"
    DATA_MUTATION = "data_mutation"
    MISSING = "missing"


@dataclass
class DocumentDiagnosis:
    name: str
    path: str
    hash_c_ok: bool
    hash_d_ok: bool
    path_exists: bool
    note: DiagnosisNote


@dataclass
class ModelDiagnosis:
    name: str
    hash_b_ok: bool
    documents: list[DocumentDiagnosis] = field(default_factory=list)


@dataclass
class StoreDiagnosis:
    hash_a_ok: bool
    models: list[ModelDiagnosis] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        bad = {DiagnosisNote.DATA_MUTATION, DiagnosisNote.MISSING}
        return (
            self.hash_a_ok
            and all(m.hash_b_ok for m in self.models)
            and all(d.note not in bad for m in self.models for d in m.documents)
        )


def _try_resolve_model(model_ref: str, pythonpath: Optional[str]) -> Optional[Type[StructuredNLDoc]]:
    from sldb.cli import _resolve_model_ref
    try:
        return _resolve_model_ref(model_ref, pythonpath)
    except SystemExit:
        return None


def diagnose_store(
    store_path: Path,
    project_root: Optional[Path] = None,
    pythonpath: Optional[str] = None,
) -> StoreDiagnosis:
    root = project_root or store_path.parent
    store_index = load_store_index(store_path)

    model_diagnoses: list[ModelDiagnosis] = []
    loaded_models_indices: list[ModelsIndex] = []

    for model_entry in store_index.models:
        models_idx = load_models_index(root / model_entry.models_index)
        docs_idx = load_documents_index(root / models_idx.documents_index)
        model_type = _try_resolve_model(model_entry.model_ref, pythonpath)

        doc_diagnoses: list[DocumentDiagnosis] = []
        for doc in docs_idx.documents:
            doc_path = root / doc.path
            if not doc_path.exists():
                doc_diagnoses.append(DocumentDiagnosis(
                    name=doc.name, path=doc.path,
                    hash_c_ok=False, hash_d_ok=False,
                    path_exists=False, note=DiagnosisNote.MISSING,
                ))
                continue

            text = doc_path.read_text(encoding="utf-8")
            hash_c_ok = hash_text(text) == doc.hash_c
            hash_d_ok = (hash_fields(model_type, text) == doc.hash_d) if model_type else True

            if hash_c_ok and hash_d_ok:
                note = DiagnosisNote.OK
            elif not hash_c_ok and hash_d_ok:
                note = DiagnosisNote.BENIGN_MUTATION
            else:
                note = DiagnosisNote.DATA_MUTATION

            doc_diagnoses.append(DocumentDiagnosis(
                name=doc.name, path=doc.path,
                hash_c_ok=hash_c_ok, hash_d_ok=hash_d_ok,
                path_exists=True, note=note,
            ))

        current_hash_b = hash_documents_index(docs_idx)
        loaded_models_indices.append(models_idx)
        model_diagnoses.append(ModelDiagnosis(
            name=models_idx.name,
            hash_b_ok=current_hash_b == models_idx.hash_b,
            documents=doc_diagnoses,
        ))

    current_hash_a = hash_models_layer(loaded_models_indices)
    return StoreDiagnosis(
        hash_a_ok=current_hash_a == store_index.hash_a,
        models=model_diagnoses,
    )
