from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional, Sequence

from sldb.store.diagnostics_models.verdict_notes import changed_fields, contract_ok as contract_stands, note as verdict_note
from sldb.store.diagnostics_models.text_history import with_history
from sldb.store.layout import project_root as store_project_root
from sldb.store.hashing import hash_documents_index, hash_models_layer, hash_text
from sldb.store.diagnostics_models.invalid_verdict import fields_state
from sldb.store.source_read import read_source_text
from sldb.store.diagnostics_models.unread_verdict import unread_diagnosis
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.legacy_contract import legacy_contract
from sldb.store.model_origin import add_owner_import_roots
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


def _diagnose_doc(doc, root: Path, model_type: Any, contract_ok: bool = True) -> DocumentDiagnosis:
    """Compare the document on disk against what the store recorded for it.

    `content` is the markdown text; `fields` is the payload extracted under the
    model's contract. Text moving while fields hold still is an expected mutation,
    so the two are reported separately rather than as one "mismatch".

    A model that cannot be imported here (`model_type` None) cannot re-extract the fields; an
    intact text then stands for intact fields, instead of reading as a data mutation that sends
    the operator to restore a file nobody touched. The model is named as unresolved.
    """
    doc_path = root / doc.path
    if (unread := unread_diagnosis(doc, root, doc_path)) is not None:
        return unread
    text = read_source_text(doc_path)
    content_on_disk = hash_text(text)
    state = fields_state(model_type, text, doc, content_on_disk)
    if isinstance(state, DocumentDiagnosis):
        return state  # the model rejects the text: nothing else of it is compared (inbox 3895e9f7 H1)
    return _compared(doc, state, content_on_disk, contract_ok)


def _compared(doc, state: tuple[str, dict[str, str], bool], content_on_disk: str, contract_ok: bool) -> DocumentDiagnosis:
    fields_on_disk, map_on_disk, fields_ok = state
    content_ok = content_on_disk == doc.source_hash
    changed = [] if fields_ok else changed_fields(getattr(doc, "field_hashes", {}) or {}, map_on_disk)
    return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=content_ok, fields_ok=fields_ok, path_exists=True, note=verdict_note(content_ok, fields_ok, contract_ok), content_on_disk=content_on_disk, content_in_index=doc.source_hash, fields_on_disk=fields_on_disk, fields_in_index=doc.content_hash, changed_fields=changed)


def _is_generated_missing(doc, root: Path, derived: Sequence[str]) -> bool:
    """A tracked document under a declared `derived` path that is not on disk: a generator writes it."""
    parts = Path(doc.path).parts
    under = any(parts[: len(Path(d).parts)] == Path(d).parts for d in derived if Path(d).parts)
    return under and not (root / doc.path).exists()


def _diagnose_model(model_entry, root, pythonpath, resolve_model_ref: Callable, derived: Sequence[str] = ()) -> tuple[ModelDiagnosis, ModelsIndex]:
    """The model node, split into the two children that can move it: its document roster and
    its contract. Attributing the node to one of them is the whole point of storing both."""
    models_idx = load_models_index(root / model_entry.models_index)
    docs_idx = load_documents_index(root / models_idx.documents_index)
    model_type = _try_resolve_model(model_entry.model_ref, pythonpath, resolve_model_ref)
    legacy = legacy_contract(models_idx, model_type)
    contract_ok = contract_stands(models_idx, docs_idx, root, model_type, legacy)
    generated = [d for d in docs_idx.documents if derived and _is_generated_missing(d, root, derived)]
    present = [d for d in docs_idx.documents if d not in generated]
    doc_diagnoses = [_with_history(_diagnose_doc(d, root, model_type, contract_ok), root) for d in present]
    roster_ok = hash_documents_index(docs_idx) == models_idx.roster_hash
    return ModelDiagnosis(name=models_idx.name, roster_ok=roster_ok, contract_ok=contract_ok, legacy_contract=legacy, resolved=model_type is not None, source_path=models_idx.path, documents=doc_diagnoses, generated_missing=len(generated)), models_idx

def _with_history(doc: DocumentDiagnosis, root: Path) -> DocumentDiagnosis:
    """The text's git history, except for a path sldb would not read (nothing to compare)."""
    return doc if doc.note in (DiagnosisNote.PATH_OUTSIDE_ROOT, DiagnosisNote.SYMLINK_NOT_READ) else with_history(doc, root)


def diagnose_store(store_path: Path, resolve_model_ref: Callable, project_root: Optional[Path] = None, pythonpath: Optional[str] = None, derived: Sequence[str] = ()) -> StoreDiagnosis:
    """Diagnoses the integrity of the entire store.

    `derived` are the declared generated path prefixes: a tracked document missing under one is
    counted (`ModelDiagnosis.generated_missing`), not diagnosed as missing."""
    root = project_root or store_project_root(store_path)
    add_owner_import_roots(store_path)  # inherited models import from their owner
    store_index = load_store_index(store_path)
    diagnoses = [_diagnose_model(m, root, pythonpath, resolve_model_ref, derived) for m in store_index.models]
    model_diagnoses = [d[0] for d in diagnoses]
    loaded_models_indices = [d[1] for d in diagnoses]
    return StoreDiagnosis(root_ok=hash_models_layer(loaded_models_indices) == store_index.hash_a, models=model_diagnoses)
