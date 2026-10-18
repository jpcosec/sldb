from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional

from sldb.store.field_set_drift import document_drifted
from sldb.store.diagnostics_models.text_history import with_history
from sldb.store.layout import project_root as store_project_root
from sldb.store.hashing import (
    hash_documents_index,
    hash_fields_with_map,
    hash_models_layer,
    hash_text,
)
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.legacy_contract import legacy_contract
from sldb.store.model_node import contract_moved
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
    if not doc_path.exists():
        return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=False, fields_ok=False, path_exists=False, note=DiagnosisNote.MISSING, content_in_index=doc.source_hash, fields_in_index=doc.content_hash)
    text = doc_path.read_text(encoding="utf-8")
    content_on_disk = hash_text(text)
    content_ok = content_on_disk == doc.source_hash
    fields_on_disk, map_on_disk, fields_ok = _fields_state(model_type, text, doc, content_ok)
    note = _note(content_ok, fields_ok, contract_ok)
    changed = [] if fields_ok else _changed_fields(getattr(doc, "field_hashes", {}) or {}, map_on_disk)
    return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=content_ok, fields_ok=fields_ok, path_exists=True, note=note, content_on_disk=content_on_disk, content_in_index=doc.source_hash, fields_on_disk=fields_on_disk, fields_in_index=doc.content_hash, changed_fields=changed)


def _fields_state(model_type: Any, text: str, doc, content_ok: bool) -> tuple[str, dict[str, str], bool]:
    """(fields hash on disk, per-field map, fields ok); without the class, intact text stands for intact fields."""
    if model_type is None:
        return "", {}, content_ok
    fields_on_disk, map_on_disk = hash_fields_with_map(model_type, text)
    return fields_on_disk, map_on_disk, fields_on_disk == doc.content_hash


def _changed_fields(in_index: dict[str, str], on_disk: dict[str, str]) -> list[str]:
    """The field names whose hashes disagree, plus those present on only one side.

    Empty when either side has no map: a store written before `field_hashes` cannot be asked
    which field moved, and saying "none" there would read as "nothing changed" when
    `content_hash` already said otherwise.
    """
    if not in_index or not on_disk:
        return []
    return sorted(name for name in set(in_index) | set(on_disk) if in_index.get(name) != on_disk.get(name))


def _note(content_ok: bool, fields_ok: bool, contract_ok: bool) -> DiagnosisNote:
    """Which verdict the two hashes earn — and who to blame when the fields disagree.

    Fields differing while the text stands still is not the document's doing when the model's
    contract moved: the same text extracts to something else now. Blaming the document there
    sent the reader to inspect a file nobody had edited.

    The contract only excuses the document while its TEXT is intact (`content_ok`). A moved
    contract on a file that was also edited is still a data mutation and still needs a human:
    letting the contract absolve it would hide a hand edit behind a safe-to-run verdict.
    """
    if content_ok and fields_ok:
        return DiagnosisNote.OK
    if fields_ok:
        return DiagnosisNote.BENIGN_MUTATION
    return DiagnosisNote.CONTRACT_MUTATION if not contract_ok and content_ok else DiagnosisNote.DATA_MUTATION

def _diagnose_model(model_entry, root, pythonpath, resolve_model_ref: Callable) -> tuple[ModelDiagnosis, ModelsIndex]:
    """The model node, split into the two children that can move it: its document roster and
    its contract. Attributing the node to one of them is the whole point of storing both."""
    models_idx = load_models_index(root / model_entry.models_index)
    docs_idx = load_documents_index(root / models_idx.documents_index)
    model_type = _try_resolve_model(model_entry.model_ref, pythonpath, resolve_model_ref)
    legacy = legacy_contract(models_idx, model_type)
    drifted = any(document_drifted(d, root, model_type) for d in docs_idx.documents)  # see sldb.store.field_set_drift
    contract_ok = (legacy or not contract_moved(models_idx, model_type)) and not drifted
    doc_diagnoses = [with_history(_diagnose_doc(d, root, model_type, contract_ok), root) for d in docs_idx.documents]
    roster_ok = hash_documents_index(docs_idx) == models_idx.roster_hash
    return ModelDiagnosis(name=models_idx.name, roster_ok=roster_ok, contract_ok=contract_ok, legacy_contract=legacy, resolved=model_type is not None, source_path=models_idx.path, documents=doc_diagnoses), models_idx

def diagnose_store(store_path: Path, resolve_model_ref: Callable, project_root: Optional[Path] = None, pythonpath: Optional[str] = None) -> StoreDiagnosis:
    """Diagnoses the integrity of the entire store."""
    root = project_root or store_project_root(store_path)
    add_owner_import_roots(store_path)  # inherited models import from their owner
    store_index = load_store_index(store_path)
    diagnoses = [_diagnose_model(m, root, pythonpath, resolve_model_ref) for m in store_index.models]
    model_diagnoses = [d[0] for d in diagnoses]
    loaded_models_indices = [d[1] for d in diagnoses]
    return StoreDiagnosis(root_ok=hash_models_layer(loaded_models_indices) == store_index.hash_a, models=model_diagnoses)
