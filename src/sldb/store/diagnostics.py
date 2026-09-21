from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional

from sldb.store.layout import project_root as store_project_root
from sldb.store.hashing import (
    hash_documents_index,
    hash_fields,
    hash_models_layer,
    hash_text,
)
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.models import ModelsIndex
from sldb.store.diagnostics_models import (
    DiagnosisNote,
    DocumentDiagnosis,
    ModelDiagnosis,
    StoreDiagnosis,
)


def _try_resolve_model(
    model_ref: str, pythonpath: Optional[str], resolve_model_ref: Callable
) -> Any:
    try:
        return resolve_model_ref(model_ref, pythonpath)
    except Exception:
        # Layer 4: Don't swallow everything, but for diagnostics we want best-effort
        return None


def _diagnose_doc(doc, root: Path, model_type: Any) -> DocumentDiagnosis:
    doc_path = root / doc.path
    if not doc_path.exists():
        return DocumentDiagnosis(name=doc.name, path=doc.path, hash_c_ok=False, hash_d_ok=False, path_exists=False, note=DiagnosisNote.MISSING)
    text = doc_path.read_text(encoding="utf-8")
    expected_c = hash_text(text)
    expected_d = hash_fields(model_type, text) if model_type else ""
    hash_c_ok, hash_d_ok = expected_c == doc.hash_c, expected_d == doc.hash_d
    note = DiagnosisNote.OK if hash_c_ok and hash_d_ok else DiagnosisNote.BENIGN_MUTATION if hash_d_ok else DiagnosisNote.DATA_MUTATION
    return DocumentDiagnosis(name=doc.name, path=doc.path, hash_c_ok=hash_c_ok, hash_d_ok=hash_d_ok, path_exists=True, note=note, hash_c_expected=expected_c, hash_c_actual=doc.hash_c, hash_d_expected=expected_d, hash_d_actual=doc.hash_d)

def _diagnose_model(model_entry, root, pythonpath, resolve_model_ref: Callable) -> tuple[ModelDiagnosis, ModelsIndex]:
    models_idx = load_models_index(root / model_entry.models_index)
    docs_idx = load_documents_index(root / models_idx.documents_index)
    model_type = _try_resolve_model(model_entry.model_ref, pythonpath, resolve_model_ref)
    doc_diagnoses = [_diagnose_doc(d, root, model_type) for d in docs_idx.documents]
    return ModelDiagnosis(name=models_idx.name, hash_b_ok=hash_documents_index(docs_idx) == models_idx.hash_b, documents=doc_diagnoses), models_idx

def diagnose_store(store_path: Path, resolve_model_ref: Callable, project_root: Optional[Path] = None, pythonpath: Optional[str] = None) -> StoreDiagnosis:
    """Diagnoses the integrity of the entire store."""
    root = project_root or store_project_root(store_path)
    store_index = load_store_index(store_path)
    diagnoses = [_diagnose_model(m, root, pythonpath, resolve_model_ref) for m in store_index.models]
    model_diagnoses = [d[0] for d in diagnoses]
    loaded_models_indices = [d[1] for d in diagnoses]
    return StoreDiagnosis(hash_a_ok=hash_models_layer(loaded_models_indices) == store_index.hash_a, models=model_diagnoses)
