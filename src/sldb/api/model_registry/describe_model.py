"""Describe one registered model: its registry record, its fields and its tracked documents."""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_registry.model_description import ModelDescription
from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary
from sldb.api.model_registry.model_class_attrs import draft_status, model_class_attrs
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.schema.field_kinds import annotation_name
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex


def describe_model(store: str | Path | None, model_name: str, pythonpath: str | None = None) -> ModelDescription:
    """Read a registered model's contract and documents.

    Only this model's class is imported, so a broken sibling model does not prevent it.

    Args:
        store: The store holding the model (path, alias, or None to discover it).
        model_name: Registered model name.
        pythonpath: Directory to import the model module from.

    Returns:
        The model's registry record, fields and documents.

    Raises:
        SLDBModelError: When the model is not registered or cannot be imported.
    """
    location = open_store(store)
    entry = _registered_entry(location.store_path, model_name)
    m_idx = load_models_index(location.project_root / entry.models_index)
    model_type = resolve_model_ref(entry.model_ref, pythonpath)
    return ModelDescription(
        **_index_fields(entry, m_idx),
        **_content_fields(location.project_root, m_idx, model_type),
        **model_class_attrs(model_type),
        **draft_status(location.store_path, model_name, pythonpath),
    )


def _index_fields(entry: ModelEntry, m_idx: ModelsIndex) -> dict:
    """The registry-record part of a description."""
    return {
        "name": entry.name,
        "model_ref": entry.model_ref,
        "path": entry.path,
        "version": m_idx.version,
        "canonical": m_idx.canonical,
        "family": m_idx.family,
        "semantics": list(m_idx.semantics),
        "base_models": list(m_idx.base_models),
    }


def _registered_entry(store_path: Path, model_name: str) -> ModelEntry:
    """The store's registry entry for a model name."""
    entry = next((m for m in load_store_index(store_path).models if m.name == model_name), None)
    if entry is None:
        raise SLDBModelError(f"Model '{model_name}' not found.")
    return entry


def _content_fields(root: Path, m_idx: ModelsIndex, model_type: type[StructuredNLDoc]) -> dict:
    """The fields and tracked documents of a description."""
    return {"fields": _field_summaries(model_type), "documents": _document_summaries(root, m_idx)}


def _field_summaries(model_type: type[StructuredNLDoc]) -> list[ModelFieldSummary]:
    """Name, annotation and description of every field, in declaration order."""
    return [ModelFieldSummary(name=name, annotation=annotation_name(info.annotation), description=info.description or "") for name, info in model_type.model_fields.items()]


def _document_summaries(root: Path, m_idx: ModelsIndex) -> list[ModelDocumentSummary]:
    """The model's tracked documents, sorted by name."""
    docs = load_documents_index(root / m_idx.documents_index).documents
    return [ModelDocumentSummary(name=d.name, path=d.path, semantic_tags=list(d.semantic_tags)) for d in sorted(docs, key=lambda item: item.name)]
