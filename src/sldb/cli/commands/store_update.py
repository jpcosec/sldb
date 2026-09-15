from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.hashing import hash_fields, hash_payload, hash_text
from sldb.store.io import load_documents_index, load_models_index, load_store_index, save_documents_index, save_models_index, store_lock
from sldb.store.models import StoreIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import RebuildReport, rebuild_semantic_indexes
from sldb.store import documents_hash

def update_store(args: Any) -> int:
    sp, root = get_store_context(args.store)
    idx = load_store_index(sp)
    skipped_models, skipped_docs, pending, changed = [], [], [], {}
    _process_models(idx, root, args.pythonpath, skipped_models, skipped_docs, pending, changed)
    sem, sec = _commit_updates(args, sp, root, idx, pending, changed)
    v = getattr(args, "verbose", False)
    _print_update_result(sp, skipped_models, skipped_docs, sem, sec, v)
    return 0 if not (skipped_models or skipped_docs) else 1

def _process_models(idx: StoreIndex, root: Path, pypath: str, skipped_models: list[str], skipped_docs: list[str], pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]]) -> None:
    for m_entry in idx.models:
        try:
            mtype = resolve_model_ref(m_entry.model_ref, pypath)
            _process_model(m_entry, mtype, root, skipped_docs, pending, changed)
        except Exception:
            skipped_models.append(m_entry.name)

def _process_model(m_entry: Any, mtype: Any, root: Path, skipped_docs: list[str], pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]]) -> None:
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    for doc in d_idx.documents:
        if _process_doc(doc, mtype, m_entry.name, root, skipped_docs):
            changed.setdefault(m_entry.name, []).append(doc)
    pending.append((m_entry, m_idx, d_idx))

def _process_doc(doc: Any, mtype: Any, m_name: str, root: Path, skipped_docs: list[str]) -> bool:
    """A hand edit is only ever seen by re-reading the file (hash_c), unavoidably, for every
    tracked document — but PLAN 15 capa 8: the expensive part, extracting hash_d, only runs
    for a document whose hash_c actually moved since the per-document hash map last knew it
    (`doc.hash_c`, the value `load_documents_index` handed back before this overwrites it)."""
    doc_path = root / doc.path
    if not doc_path.exists():
        skipped_docs.append(doc.name)
        return False
    text = doc_path.read_text(encoding="utf-8")
    if (new_hash_c := hash_text(text)) == doc.hash_c:
        return False
    doc.hash_c, doc.hash_d = new_hash_c, _field_hash(mtype, m_name, doc, text)
    return True

def _field_hash(mtype: Any, m_name: str, doc: Any, text: str) -> str:
    from sldb.store.runtime_cache import payload_of
    payload = payload_of(doc.path, doc.hash_c, m_name)
    try:
        return hash_payload(payload) if payload is not None else hash_fields(mtype, text)
    except Exception:
        return ""

def _commit_updates(args: Any, sp: Path, root: Path, idx: StoreIndex, pending: list[tuple[Any, Any, Any]], changed: dict[str, list[Any]]) -> tuple[RebuildReport, RebuildReport]:
    wait = getattr(args, "wait", False)
    with store_lock(sp, wait=wait):
        for m_entry, m_idx, d_idx in pending:
            save_documents_index(root / m_idx.documents_index, d_idx)
            for doc in changed.get(m_entry.name, []):
                documents_hash.note(sp, m_entry.name, doc)  # the map now agrees with what was just saved
            m_idx.hash_b = documents_hash.hash_b_of(sp, m_entry.name)
            m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
            save_models_index(root / m_entry.models_index, m_idx)
        return _rebuild_indexes(sp, root, idx, args.pythonpath)

def _rebuild_indexes(sp: Path, root: Path, idx: StoreIndex, pypath: str) -> tuple[RebuildReport, RebuildReport]:
    sem_report = rebuild_semantic_indexes(sp, root, resolve_model_ref, pypath)
    sec_report = rebuild_sections_indexes(sp, root, resolve_model_ref, pypath)
    cascade_hash_a(sp, root, idx)
    return sem_report, sec_report

def _print_update_result(sp: Path, skipped_models: list[str], skipped_docs: list[str], sem_report: RebuildReport, sec_report: RebuildReport, verbose: bool) -> None:
    print(f"Updated store at {sp}")
    if skipped_models:
        print(f"Skipped broken models: {', '.join(skipped_models)}")
    if skipped_docs:
        print(f"Skipped missing documents: {', '.join(skipped_docs)}")
    _print_reports(sem_report, sec_report, verbose)

def _print_reports(sem_report: RebuildReport, sec_report: RebuildReport, verbose: bool) -> None:
    print(f"Semantic index: {sem_report.docs_processed} processed, {sem_report.docs_skipped_missing} missing")
    print(f"Sections index: {sec_report.docs_processed} processed, {sec_report.docs_skipped_missing} missing, {sec_report.docs_empty_sections} empty, {sec_report.headings_no_map} unparseable headings")
    if verbose:
        for line in sem_report.verbose + sec_report.verbose:
            print(f"  {line}")
