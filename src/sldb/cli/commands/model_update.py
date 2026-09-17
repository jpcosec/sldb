from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.hashing import hash_documents_index, hash_fields, hash_text
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    store_lock,
)
from sldb.store.ops import cascade_hash_a
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.core.exceptions import SLDBModelError


def update_model(args: Any) -> int:
    sp, root = get_store_context(args.store)
    idx = load_store_index(sp)
    m_entry = _get_model_entry(idx, args.model)
    _update_model(args, sp, root, idx, m_entry)
    return 0

def _get_model_entry(idx: Any, name: str) -> Any:
    m_entry = next((m for m in idx.models if m.name == name), None)
    if not m_entry:
        raise SLDBModelError(f"Model '{name}' not found.")
    return m_entry

def _update_model(args: Any, sp: Path, root: Path, idx: Any, m_entry: Any) -> None:
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    model_type = resolve_model_ref(m_entry.model_ref, args.pythonpath)
    _update_docs_hashes(root, d_idx, model_type)
    with store_lock(sp):
        _save_updated_indexes(args, root, m_entry, m_idx, d_idx)
        _finalize_store_update(sp, root, idx, args.pythonpath)
    print(f"Updated '{args.model}'")

def _update_docs_hashes(root: Path, d_idx: Any, model_type: type) -> None:
    for doc in d_idx.documents:
        _update_doc_hash(root, doc, model_type)

def _update_doc_hash(root: Path, doc: Any, model_type: type) -> None:
    text = (root / doc.path).read_text(encoding="utf-8")
    doc.hash_c = hash_text(text)
    try:
        doc.hash_d = hash_fields(model_type, text)
    except Exception:
        doc.hash_d = ""

def _save_updated_indexes(args: Any, root: Path, m_entry: Any, m_idx: Any, d_idx: Any) -> None:
    save_documents_index(root / m_idx.documents_index, d_idx)
    if getattr(args, "bump_version", False):
        m_idx.version += 1
        m_entry.version = m_idx.version
    m_idx.hash_b = hash_documents_index(d_idx)
    save_models_index(root / m_entry.models_index, m_idx)

def _finalize_store_update(sp: Path, root: Path, idx: Any, pythonpath: str) -> None:
    rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
    cascade_hash_a(sp, root, idx)
