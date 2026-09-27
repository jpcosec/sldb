"""Rehash every tracked document of a store whose Markdown changed since it was indexed.

Moved here from `sldb.cli.commands.store_update`, which re-exports these names.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.hashing import hash_fields, hash_payload, hash_text
from sldb.store.model_node import contract_moved
from sldb.store.io import load_documents_index, load_models_index
from sldb.store.models.store_index import StoreIndex


def _process_models(idx: StoreIndex, root: Path, pypath: str | None, skipped_models: list[str], skipped_docs: list[str], pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]]) -> None:
    """Rehash every model's documents; a model whose class fails to import is recorded as skipped.

    The broad catch isolates one broken model module (it may raise anything on import)
    from the rest of the store, and records it in `skipped_models` for the report.
    """
    for m_entry in idx.models:
        try:
            mtype = resolve_model_ref(m_entry.model_ref, pypath)
            _process_model(m_entry, mtype, root, skipped_docs, pending, changed)
        except Exception:
            skipped_models.append(m_entry.name)


def _process_model(m_entry: Any, mtype: Any, root: Path, skipped_docs: list[str], pending: list[tuple[Any, Any, Any, Any]], changed: dict[str, list[Any]]) -> None:
    """Rehash one model's documents and queue its indexes to be saved.

    A contract that moved forces every document of the model through extraction again, even
    where the Markdown is untouched: a field added to the class, or a changed template, makes
    the same text yield a different payload, and no `source_hash` moves to say so.
    """
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    force = contract_moved(m_idx, mtype)
    for doc in d_idx.documents:
        if _process_doc(doc, mtype, m_entry.name, root, skipped_docs, force):
            changed.setdefault(m_entry.name, []).append(doc)
    pending.append((m_entry, m_idx, d_idx, mtype))


def _process_doc(doc: Any, mtype: Any, m_name: str, root: Path, skipped_docs: list[str], force: bool = False) -> bool:
    """Rehash one document when its Markdown changed; False when unchanged or missing.

    A hand edit is only ever seen by re-reading the file (source_hash), unavoidably, for every
    tracked document — but PLAN 15 capa 8: the expensive part, extracting content_hash, only
    runs for a document whose source_hash actually moved since the per-document hash map last
    knew it. `force` is the one case where the text is not the trigger: the model's contract
    moved, so the payload can change with the text standing still.
    """
    doc_path = root / doc.path
    if not doc_path.exists():
        skipped_docs.append(doc.name)
        return False
    text = doc_path.read_text(encoding="utf-8")
    if (fresh := hash_text(text)) == doc.source_hash and not force:
        return False
    doc.source_hash, doc.content_hash = fresh, _field_hash(mtype, m_name, doc, text, force)
    return True


def _field_hash(mtype: Any, m_name: str, doc: Any, text: str, force: bool = False) -> str:
    """Hash of the document's fields; empty when the Markdown no longer extracts (reported by `stores check`).

    The cached payload is skipped when the contract moved: it was extracted under the previous
    contract, which is exactly what must not win here.
    """
    from sldb.store.runtime_cache import payload_of
    payload = None if force else payload_of(doc.path, doc.source_hash, mtype)
    try:
        return hash_payload(payload) if payload is not None else hash_fields(mtype, text)
    except Exception:
        return ""
