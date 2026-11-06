"""The steps of `save_document_payload`, moved here from `sldb.cli.commands.fields_save`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBModelError, SLDBPayloadSaveError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store import documents_hash
from sldb.store.hashing import hash_fields_with_map, hash_text
from sldb.store.io import load_models_index, load_store_index, save_models_index, store_lock
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex
from sldb.store.model_node import stamp_model_node
from sldb.store.ops import cascade_store_hash
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes


def model_class(model_ref: str, pythonpath: str | None, root: Path) -> type:
    """The model class, imported with the caller's pythonpath first, then the store's own root.

    A linked store's models import from where that store lives.
    """
    try:
        return resolve_model_ref(model_ref, pythonpath)
    except SLDBModelError:
        return resolve_model_ref(model_ref, str(root))


def load_model_indexes(sp: Path, root: Path, model_name: str) -> tuple[StoreIndex, ModelEntry, ModelsIndex]:
    """The store index, the model's entry and its models index."""
    idx = load_store_index(sp)
    m_entry = next((m for m in idx.models if m.name == model_name), None)
    if m_entry is None:
        raise SLDBPayloadSaveError(f"Model '{model_name}' not registered.")
    return idx, m_entry, load_models_index(root / m_entry.models_index)


def load_document_entry(sp: Path, model_name: str, doc_name: str) -> DocumentEntry:
    """The document's index entry, from its shard."""
    doc_entry = load_document_shard(documents_shard_path(sp, model_name, doc_name))
    if doc_entry is None:
        raise SLDBPayloadSaveError(f"Doc '{doc_name}' not registered.")
    return doc_entry


def render_checked(model_type: type, payload: dict[str, Any], ref_root: Path, store_path: Path | None = None) -> str:
    """The payload rendered to Markdown, refused unless it round-trips.

    `ref_root` is the project root, so a composed field resolves its refs against the project
    rather than against whatever directory the caller happens to run in. With `store_path`, the
    unpinned document anchors of the payload are pinned first (GO07, `doc_anchor_pinning`).
    """
    from sldb.api.documents.doc_anchor_pinning import pin_payload

    payload = pin_payload(store_path, model_type, payload) if store_path is not None else payload
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBPayloadSaveError(f"Field mutation broke idempotency: {details}")
    return rendered


def check_rules_on_write(store_path: Path, model_type: type, node: str, payload: dict[str, Any]) -> None:
    """The `on_write` rules on the pinned payload of `node` (GO08), before anything is written:
    an error raises `SLDBRuleViolationError`; a store without RuleDoc is not read."""
    from sldb.api.rules.rules_on_write import check_on_write

    check_on_write(store_path, model_type, node, payload)


def write_rendered_document(root: Path, doc_entry: DocumentEntry, model_type: type, rendered: str, via: str = "save_document_payload", actor: str | None = None, store_path: Path | None = None) -> None:
    """Write the rendered Markdown, signed with its provenance block (plus final newline), and
    record its source and content hashes. With `store_path`, the block's unpinned `from:`
    document anchors are pinned (GO07)."""
    from sldb.api.documents.doc_anchor_pinning import pin_provenance
    from sldb.api.documents.provenance_stamp import stamped_file
    from sldb.models.provenance_block import index_block

    text = stamped_file(root / doc_entry.path, rendered + "\n", model_type, via, actor)
    text = pin_provenance(store_path, text) if store_path is not None else text
    (root / doc_entry.path).write_text(text, encoding="utf-8")
    doc_entry.source_hash = hash_text(text)
    doc_entry.content_hash, doc_entry.field_hashes = hash_fields_with_map(model_type, text)
    doc_entry.provenance = index_block(text)


def save_document_indexes(sp: Path, root: Path, idx: StoreIndex, m_idx: ModelsIndex, m_entry: ModelEntry, doc_entry: DocumentEntry, pythonpath: str | None, model_type: type | None = None) -> None:
    """Save the document shard and model hashes, then rebuild derived indexes, under the store lock.

    The model's roster hash covers its documents' hashes: a field write must move it, or
    `stores check` fails and consumers keyed on the model node never see the change.
    """
    with store_lock(sp):
        save_document_shard(documents_shard_path(sp, m_entry.name, doc_entry.name), doc_entry)
        documents_hash.note(sp, m_entry.name, doc_entry)
        stamp_model_node(m_idx, documents_hash.roster_hash_of(sp, m_entry.name), model_type)
        m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)
        rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_sections_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_edges_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_store_hash(sp, root, idx)
