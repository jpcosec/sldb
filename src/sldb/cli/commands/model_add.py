from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.hashing import hash_documents_index
from sldb.store.io import load_store_index, save_documents_index, save_models_index, store_lock
from sldb.store.layout import documents_index_relpath, models_index_relpath
from sldb.store.models import DocumentsIndex, ModelEntry, ModelsIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store.semantic_tags import flatten_model_semantics
from sldb.core.exceptions import SLDBModelError
from sldb.api.model_registry.model_lineage import model_base_names, model_family  # moved to sldb.api.model_registry; re-exported


def add_model(args: Any) -> int:
    sp, root = get_store_context(args.store)
    model_type = resolve_model_ref(args.model, args.pythonpath)
    idx = load_store_index(sp)
    if _model_exists(idx, model_type.__name__):
        print(f"Model '{model_type.__name__}' already registered.")
        return 0
    _register_model(args, sp, root, idx, model_type)
    return 0

def _get_rel_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path.resolve())

def _model_exists(idx: Any, name: str) -> bool:
    return any(m.name == name for m in idx.models)

def _register_model(args: Any, sp: Path, root: Path, idx: Any, model_type: type) -> None:
    with store_lock(sp):
        _write_model_indexes(args, sp, root, idx, model_type)
        _finalize_store_update(sp, root, idx, args.pythonpath)
    print(f"Registered '{model_type.__name__}'")

def _write_model_indexes(args: Any, sp: Path, root: Path, idx: Any, model_type: type) -> None:
    m_path = _get_rel_path(Path(inspect.getfile(model_type)), root)
    mi_rel = models_index_relpath(sp, model_type.__name__)
    di_rel = documents_index_relpath(sp, model_type.__name__)
    empty_documents = DocumentsIndex()
    save_documents_index(root / di_rel, empty_documents)
    mi = _create_models_index(args, model_type, m_path, di_rel, empty_documents)
    save_models_index(root / mi_rel, mi)
    idx.models.append(_create_model_entry(args, mi.name, m_path, mi_rel))

def _create_models_index(args: Any, model_type: type, path: str, di_rel: str, documents_index: DocumentsIndex) -> ModelsIndex:
    # hash_b must match hash_documents_index(documents_index) from the start, even
    # for a freshly registered model with zero documents -- otherwise `stores
    # check` reports a false DATA_MUTATION-shaped failure (hash_b_ok=False)
    # against a store that was never actually mutated, until someone happens to
    # run `models update` once. See hash_documents_index(DocumentsIndex()) for
    # what an empty index's real hash looks like; it is not the empty string.
    return ModelsIndex(
        name=model_type.__name__, model_ref=args.model, path=path,
        documents_index=di_rel, hash_b=hash_documents_index(documents_index), version=1, canonical=args.canonical,
        family=model_family(model_type), semantics=flatten_model_semantics(model_type),
        base_models=model_base_names(model_type),
    )

def _create_model_entry(args: Any, name: str, path: str, mi_rel: str) -> ModelEntry:
    return ModelEntry(
        name=name, model_ref=args.model, path=path, models_index=mi_rel, version=1
    )

def _finalize_store_update(sp: Path, root: Path, idx: Any, pythonpath: str) -> None:
    rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
    cascade_hash_a(sp, root, idx)
