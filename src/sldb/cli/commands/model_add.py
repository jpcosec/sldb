from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.io import load_store_index, save_documents_index, save_models_index, store_lock
from sldb.store.layout import documents_index_relpath, models_index_relpath
from sldb.store.models import DocumentsIndex, ModelEntry, ModelsIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.semantic import rebuild_semantic_indexes
from sldb.store.semantic_tags import flatten_model_semantics
from sldb.core.exceptions import SLDBModelError


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
        _write_model_indexes(args, root, idx, model_type)
        _finalize_store_update(sp, root, idx, args.pythonpath)
    print(f"Registered '{model_type.__name__}'")

def _write_model_indexes(args: Any, root: Path, idx: Any, model_type: type) -> None:
    m_path = _get_rel_path(Path(inspect.getfile(model_type)), root)
    mi_rel = models_index_relpath(model_type.__name__)
    di_rel = documents_index_relpath(model_type.__name__)
    save_documents_index(root / di_rel, DocumentsIndex())
    mi = _create_models_index(args, model_type, m_path, di_rel)
    save_models_index(root / mi_rel, mi)
    idx.models.append(_create_model_entry(args, mi.name, m_path, mi_rel))

def _create_models_index(args: Any, model_type: type, path: str, di_rel: str) -> ModelsIndex:
    return ModelsIndex(
        name=model_type.__name__, model_ref=args.model, path=path,
        documents_index=di_rel, hash_b="", version=1, canonical=args.canonical,
        family=model_family(model_type), semantics=flatten_model_semantics(model_type),
        base_models=model_base_names(model_type),
    )

def _create_model_entry(args: Any, name: str, path: str, mi_rel: str) -> ModelEntry:
    return ModelEntry(
        name=name, model_ref=args.model, path=path, models_index=mi_rel, version=1
    )

def model_family(model_type: type) -> str | None:
    """The model's declared `__family__`, the root branch it belongs to."""
    value = getattr(model_type, "__family__", None)
    return str(value) if value else None

def model_base_names(model_type: type) -> list[str]:
    """Names of the StructuredNLDoc bases above this model, nearest first.

    Recorded so `st.{Base+}` families and `model <= Base` filters are legible from the
    store index without importing the class."""
    from sldb.models.structured_doc import StructuredNLDoc
    return [
        base.__name__ for base in model_type.__mro__[1:]
        if isinstance(base, type) and issubclass(base, StructuredNLDoc) and base is not StructuredNLDoc
    ]

def _finalize_store_update(sp: Path, root: Path, idx: Any, pythonpath: str) -> None:
    rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
    cascade_hash_a(sp, root, idx)
