"""Recompute a registered model's document hashes after its class or documents changed."""

from __future__ import annotations

from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_registry.model_index_writes import rehash_documents, save_reindexed_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.schema.describe_field import schema_snapshot
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.store_index import StoreIndex


def reindex_model(store: str | Path | None, model_name: str, pythonpath: str | None = None, bump_version: bool = False, actor: str | None = None) -> ModelRegistration:
    """Rehash every document of a model and rebuild the store's derived indexes.

    Args:
        store: The store holding the model (path, alias, or None to discover it).
        model_name: Registered model name.
        pythonpath: Directory to import the model module from.
        bump_version: Increase the model's contract version (done when a draft is promoted).
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The model's registry record after the reindex.

    Raises:
        SLDBModelError: When the model is not registered or cannot be imported.
    """
    location = open_store(store)
    idx = load_store_index(location.store_path)
    m_entry = _model_entry(idx, model_name)
    m_idx = load_models_index(location.project_root / m_entry.models_index)
    d_idx = load_documents_index(location.project_root / m_idx.documents_index)
    _rehash_and_record(location, idx, m_entry, m_idx, d_idx, pythonpath, bump_version, actor)
    return ModelRegistration(name=m_entry.name, model_ref=m_entry.model_ref, path=m_entry.path, version=m_idx.version)


def _rehash_and_record(location, idx: StoreIndex, m_entry: ModelEntry, m_idx, d_idx, pythonpath: str | None, bump_version: bool, actor: str | None) -> None:
    before = store_hash(location.store_path)
    model_type = resolve_model_ref(m_entry.model_ref, pythonpath)
    before_version = m_idx.version
    rehash_documents(location.project_root, d_idx, model_type)
    save_reindexed_model(location.store_path, location.project_root, idx, m_entry, m_idx, d_idx, bump_version, pythonpath)
    _record_entry(location.store_path, m_entry, model_type, before_version, m_idx.version, before, actor)


def _record_entry(sp: Path, m_entry: ModelEntry, model_type: type, before_version: int, after_version: int, before: str, actor: str | None) -> None:
    record(sp, {"operation": "reindex_model", "address": m_entry.name, "previous_value": schema_snapshot(model_type, before_version), "new_value": schema_snapshot(model_type, after_version), "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})


def _model_entry(idx: StoreIndex, model_name: str) -> ModelEntry:
    """The registry entry of a model name."""
    m_entry = next((m for m in idx.models if m.name == model_name), None)
    if not m_entry:
        raise SLDBModelError(f"Model '{model_name}' not found.")
    return m_entry
