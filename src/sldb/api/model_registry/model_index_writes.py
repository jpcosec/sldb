"""Write the indexes of a newly registered model and of a reindexed one."""

from __future__ import annotations

from pathlib import Path
from sldb.api.model_registry.model_lineage import model_base_names, model_family
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store import documents_hash
from sldb.store.hashing import hash_documents_index, hash_fields, hash_text
from sldb.store.io import save_documents_index, save_models_index, store_lock
from sldb.store.models.documents_index import DocumentsIndex
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store.semantic_tags import flatten_model_semantics


def relative_model_path(path: Path, root: Path) -> str:
    """Model source path relative to the project root when inside it, else absolute."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path.resolve())


def write_new_model_indexes(sp: Path, root: Path, idx: StoreIndex, model_type: type, model_ref: str, m_path: str, mi_rel: str, di_rel: str, canonical: bool, pythonpath: str | None) -> ModelsIndex:
    """Register a model: empty documents index, models index, store entry, semantic rebuild.

    hash_b starts as hash_documents_index of the empty index, not "" -- an unhashed empty
    string fails `stores check` until `models update` runs.
    """
    with store_lock(sp):
        empty_documents = DocumentsIndex()
        save_documents_index(root / di_rel, empty_documents)
        family, bases = model_family(model_type), model_base_names(model_type)
        mi = ModelsIndex(name=model_type.__name__, model_ref=model_ref, path=m_path, documents_index=di_rel, hash_b=hash_documents_index(empty_documents), version=1, canonical=canonical, family=family, semantics=flatten_model_semantics(model_type), base_models=bases)
        save_models_index(root / mi_rel, mi)
        idx.models.append(ModelEntry(name=mi.name, model_ref=model_ref, path=m_path, models_index=mi_rel, version=1, family=family, semantics=mi.semantics))
        rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_hash_a(sp, root, idx)
    return mi


def rehash_documents(root: Path, d_idx: DocumentsIndex, model_type: type) -> None:
    """Recompute every document's content and field hashes from its Markdown file.

    A document that no longer extracts gets an empty field hash, which `stores check`
    reports; the broad catch keeps one bad document from aborting the whole reindex.
    """
    for doc in d_idx.documents:
        text = (root / doc.path).read_text(encoding="utf-8")
        doc.hash_c = hash_text(text)
        try:
            doc.hash_d = hash_fields(model_type, text)
        except Exception:
            doc.hash_d = ""


def save_reindexed_model(sp: Path, root: Path, idx: StoreIndex, m_entry: ModelEntry, m_idx: ModelsIndex, d_idx: DocumentsIndex, bump_version: bool, pythonpath: str | None) -> None:
    """Persist a reindexed model's indexes (bumping its version if asked) and rebuild derived indexes."""
    with store_lock(sp):
        save_documents_index(root / m_idx.documents_index, d_idx)
        if bump_version:
            _bump_version(m_idx, m_entry)
        m_idx.hash_b = hash_documents_index(d_idx)
        m_idx.documents_count = len(d_idx.documents)
        save_models_index(root / m_entry.models_index, m_idx)
        documents_hash.invalidate(sp, m_entry.name)  # a full scan just moved hash_c/hash_d
        rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_hash_a(sp, root, idx)


def _bump_version(m_idx: ModelsIndex, m_entry: ModelEntry) -> None:
    """Increase the model's contract version in both its models index and its store entry."""
    m_idx.version += 1
    m_entry.version = m_idx.version
