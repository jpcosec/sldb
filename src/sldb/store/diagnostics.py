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
    """Compare the document on disk against what the store recorded for it.

    `content` is the markdown text; `fields` is the payload extracted under the
    model's contract. Text moving while fields hold still is an expected mutation,
    so the two are reported separately rather than as one "mismatch".
    """
    doc_path = root / doc.path
    if not doc_path.exists():
        return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=False, fields_ok=False, path_exists=False, note=DiagnosisNote.MISSING, content_in_index=doc.hash_c, fields_in_index=doc.hash_d)
    text = doc_path.read_text(encoding="utf-8")
    content_on_disk = hash_text(text)
    fields_on_disk = hash_fields(model_type, text) if model_type else ""
    content_ok, fields_ok = content_on_disk == doc.hash_c, fields_on_disk == doc.hash_d
    note = DiagnosisNote.OK if content_ok and fields_ok else DiagnosisNote.BENIGN_MUTATION if fields_ok else DiagnosisNote.DATA_MUTATION
    return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=content_ok, fields_ok=fields_ok, path_exists=True, note=note, content_on_disk=content_on_disk, content_in_index=doc.hash_c, fields_on_disk=fields_on_disk, fields_in_index=doc.hash_d)

def _diagnose_model(model_entry, root, pythonpath, resolve_model_ref: Callable) -> tuple[ModelDiagnosis, ModelsIndex]:
    models_idx = load_models_index(root / model_entry.models_index)
    docs_idx = load_documents_index(root / models_idx.documents_index)
    model_type = _try_resolve_model(model_entry.model_ref, pythonpath, resolve_model_ref)
    doc_diagnoses = [_diagnose_doc(d, root, model_type) for d in docs_idx.documents]
    return ModelDiagnosis(name=models_idx.name, roster_ok=hash_documents_index(docs_idx) == models_idx.hash_b, documents=doc_diagnoses), models_idx

def diagnose_store(store_path: Path, resolve_model_ref: Callable, project_root: Optional[Path] = None, pythonpath: Optional[str] = None) -> StoreDiagnosis:
    """Diagnoses the integrity of the entire store."""
    root = project_root or store_project_root(store_path)
    store_index = load_store_index(store_path)
    diagnoses = [_diagnose_model(m, root, pythonpath, resolve_model_ref) for m in store_index.models]
    model_diagnoses = [d[0] for d in diagnoses]
    loaded_models_indices = [d[1] for d in diagnoses]
    return StoreDiagnosis(root_ok=hash_models_layer(loaded_models_indices) == store_index.hash_a, models=model_diagnoses)
