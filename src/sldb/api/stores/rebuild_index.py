"""`sldb stores rebuild-index`: `core/store_index.yaml` and `core/models/*.yaml` regenerated
from the document shards and each model's contract, whatever git left in them (and `store.yaml`'s include rules joined
when git left conflict markers there too).

Every hash is recomputed (roster from the shards, contract from the class, model node, store
root) and `documents_count` is counted again; only what the indexes register (which models,
links, predicates) is read back, repaired first when git left conflict markers in it."""

from __future__ import annotations

from pathlib import Path

import yaml

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.derived_recovery import recovered_data
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_declaration import declaration_path
from sldb.api.stores.store_file_merge import merge_declaration_data, merge_index_data
from sldb.store.io.derived_guard import has_conflict_markers
from sldb.store import documents_hash
from sldb.store.io import invalidate_index_cache, save_models_index, save_store_index, store_lock
from sldb.store.io.shard_compose import compose_documents_entries
from sldb.store.layout import project_root, store_index_path
from sldb.store.model_node import stamp_model_node
from sldb.store.models import ModelsIndex, StoreIndex
from sldb.store.ops import cascade_store_hash


def rebuild_index(store: str | Path | None = None) -> dict[str, list[str]]:
    """Regenerate both derived levels of the store's index.

    Args:
        store: The `.sldb` directory (or its project), or None for the nearest one.

    Returns:
        `repaired`: the files that had conflict markers or did not parse; `models`: every
        model whose node was recomputed.
    """
    store_path, repaired = locate_store(store), []
    with store_lock(store_path, wait=True):
        _repair_declaration(store_path, repaired)
        index = _recover_store_index(store_path, repaired)
        indexes = [_recover_model_index(store_path, entry, repaired) for entry in index.models]
        open_store(store_path)  # reads the indexes: only once both levels parse again
        models = [_rebuild_model(store_path, entry, m_idx) for entry, m_idx in zip(index.models, indexes)]
        cascade_store_hash(store_path, project_root(store_path), index)
    invalidate_index_cache()
    return {"repaired": repaired, "models": models}


def locate_store(store: str | Path | None) -> Path:
    """The store directory, found without reading its (possibly broken) index."""
    start = Path(store).resolve() if store else Path.cwd().resolve()
    for folder in (start, *start.parents):
        for candidate in (folder, folder / ".sldb"):
            if store_index_path(candidate).is_file():
                return candidate
    raise FileNotFoundError(f"No .sldb/core/store_index.yaml at or above {start}")


def _repair_declaration(store_path: Path, repaired: list[str]) -> None:
    """`store.yaml` is source, not derived, but conflict markers in it are only two include
    lists side by side: joined as the merge driver joins them (`merge_declaration_data`)."""
    path = declaration_path(store_path)
    if path.is_file() and has_conflict_markers(path.read_text(encoding="utf-8", errors="replace")):
        data, _ = recovered_data(path, merge_declaration_data)
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
        repaired.append(str(path))


def _recover_store_index(store_path: Path, repaired: list[str]) -> StoreIndex:
    data, broken = recovered_data(store_index_path(store_path), merge_index_data)
    index = StoreIndex(**data)
    if broken:
        repaired.append(str(store_index_path(store_path)))
        save_store_index(store_path, index)
    return index


def _recover_model_index(store_path: Path, entry, repaired: list[str]) -> ModelsIndex:
    """The model's index as registered (this branch's side when git left markers), saved back
    when it had to be repaired; its hashes are recomputed afterwards by `_rebuild_model`."""
    path = project_root(store_path) / entry.models_index
    data, broken = recovered_data(path, lambda ours, theirs: ours)
    m_idx = ModelsIndex(**data)
    if broken:
        repaired.append(str(path))
        save_models_index(path, m_idx)
    return m_idx


def _rebuild_model(store_path: Path, entry, m_idx: ModelsIndex) -> str:
    """One model node: roster and count from its shards, contract from its class when it imports."""
    entries = {e.name: e for e in compose_documents_entries(store_path, entry.name)}
    stamp_model_node(m_idx, documents_hash._hash_b(entries), _model_type(entry.model_ref, store_path), entry)
    m_idx.documents_count = len(entries)
    save_models_index(project_root(store_path) / entry.models_index, m_idx)
    documents_hash.invalidate(store_path, entry.name)
    return entry.name


def _model_type(model_ref: str, store_path: Path):
    try:
        return resolve_model_ref(model_ref, str(project_root(store_path)))
    except Exception:  # an unimportable or federated class keeps the contract the index signed
        return None
