from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.hashing import hash_documents_index, hash_fields, hash_text
from sldb.store.io import load_documents_index, load_models_index, load_store_index, save_documents_index, save_models_index, store_lock
from sldb.store.models import StoreIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import RebuildReport, rebuild_semantic_indexes

def update_store(args: Any) -> int:
    sp, root = get_store_context(args.store)
    idx = load_store_index(sp)
    skipped_models, skipped_docs, pending = [], [], []
    _process_models(idx, root, args.pythonpath, skipped_models, skipped_docs, pending)
    sem, sec = _commit_updates(args, sp, root, idx, pending)
    v = getattr(args, "verbose", False)
    _print_update_result(sp, skipped_models, skipped_docs, sem, sec, v)
    return 0 if not (skipped_models or skipped_docs) else 1

def _process_models(idx: StoreIndex, root: Path, pypath: str, skipped_models: list[str], skipped_docs: list[str], pending: list[tuple[Any, Any, Any]]) -> None:
    for m_entry in idx.models:
        try:
            mtype = resolve_model_ref(m_entry.model_ref, pypath)
            _process_model(m_entry, mtype, root, skipped_docs, pending)
        except Exception:
            skipped_models.append(m_entry.name)

def _process_model(m_entry: Any, mtype: Any, root: Path, skipped_docs: list[str], pending: list[tuple[Any, Any, Any]]) -> None:
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    for doc in d_idx.documents:
        _process_doc(doc, mtype, root, skipped_docs)
    pending.append((m_entry, m_idx, d_idx))

def _process_doc(doc: Any, mtype: Any, root: Path, skipped_docs: list[str]) -> None:
    doc_path = root / doc.path
    if not doc_path.exists():
        return skipped_docs.append(doc.name)
    text = doc_path.read_text(encoding="utf-8")
    hash_c = hash_text(text)
    if hash_c == doc.hash_c and doc.hash_d:
        return None   # the text did not change since the last update: its field hash stands
    doc.hash_c, doc.hash_d = hash_c, _field_hash(mtype, text)

def _field_hash(mtype: Any, text: str) -> str:
    try:
        return hash_fields(mtype, text)
    except Exception:
        return ""

def _commit_updates(args: Any, sp: Path, root: Path, idx: StoreIndex, pending: list[tuple[Any, Any, Any]]) -> tuple[RebuildReport, RebuildReport]:
    wait = getattr(args, "wait", False)
    with store_lock(sp, wait=wait):
        for m_entry, m_idx, d_idx in pending:
            save_documents_index(root / m_idx.documents_index, d_idx)
            m_idx.hash_b = hash_documents_index(d_idx)
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
