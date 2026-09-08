from typing import Any
from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.hashing import hash_documents_index, hash_fields, hash_text
from sldb.store.io import (
    load_documents_index, load_models_index, load_store_index,
    save_documents_index, save_models_index, store_lock
)
from sldb.store.ops import cascade_hash_a
from sldb.store.semantic import rebuild_semantic_indexes

def save_payload(runtime_doc: Any, payload: dict[str, Any], store_arg: str | None, pythonpath: str | None) -> int:
    sp, root = get_store_context(store_arg)
    idx, m_entry, m_idx = _load_model_indices(sp, root, runtime_doc.model_name)
    d_idx, doc_entry = _load_doc_indices(root, m_idx, runtime_doc.name)
    model_type = resolve_model_ref(m_entry.model_ref, pythonpath)
    rendered = _render_and_validate(model_type, payload)
    _update_doc_entry(root, doc_entry, model_type, rendered)
    _save_indices(sp, root, idx, m_idx, m_entry, d_idx, pythonpath)
    print(f"Updated field payload for '{runtime_doc.name}'")
    return 0

def _load_model_indices(sp: Any, root: Any, model_name: str) -> tuple[Any, Any, Any]:
    idx = load_store_index(sp)
    m_entry = next((m for m in idx.models if m.name == model_name), None)
    if m_entry is None: raise SystemExit(f"Model '{model_name}' not registered.")
    m_idx = load_models_index(root / m_entry.models_index)
    return idx, m_entry, m_idx

def _load_doc_indices(root: Any, m_idx: Any, doc_name: str) -> tuple[Any, Any]:
    d_idx = load_documents_index(root / m_idx.documents_index)
    doc_entry = next((d for d in d_idx.documents if d.name == doc_name), None)
    if doc_entry is None: raise SystemExit(f"Doc '{doc_name}' not registered.")
    return d_idx, doc_entry

def _render_and_validate(model_type: type, payload: dict[str, Any]) -> str:
    rendered = render_model_markdown(model_type, payload)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid: raise SystemExit(f"Field mutation broke idempotency: {details}")
    return rendered

def _update_doc_entry(root: Any, doc_entry: Any, model_type: type, rendered: str) -> None:
    doc_path = root / doc_entry.path
    doc_path.write_text(rendered + "\n", encoding="utf-8")
    doc_entry.hash_c = hash_text(rendered + "\n")
    doc_entry.hash_d = hash_fields(model_type, rendered + "\n")

def _save_indices(sp: Any, root: Any, idx: Any, m_idx: Any, m_entry: Any, d_idx: Any, pythonpath: str | None) -> None:
    with store_lock(sp):
        save_documents_index(root / m_idx.documents_index, d_idx)
        # the model's hash_b covers its documents' hashes: a field write must move it,
        # or `stores check` fails and consumers keyed on hash_b never see the change
        m_idx.hash_b = hash_documents_index(d_idx)
        save_models_index(root / m_entry.models_index, m_idx)
        rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_hash_a(sp, root, idx)
