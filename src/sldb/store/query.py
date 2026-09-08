from __future__ import annotations

from pathlib import Path

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.layout import project_root, store_exists
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
)
from sldb.store.query_engine.models import RuntimeDocument
from sldb.store.runtime_cache import cached_document, cached_store, invalidate_runtime_cache  # noqa: F401


def _resolve_path(base: Path, maybe_relative: str) -> Path:
    """Resolves a potentially relative path against a base path."""
    path = Path(maybe_relative)
    return path if path.is_absolute() else (base / path).resolve()


def _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec: StoreCodec) -> RuntimeDocument | None:
    d_path = root / doc.path
    if not d_path.exists():
        return None
    return RuntimeDocument(store_name=s_name, store_path=s_path, model_name=m_entry.name, model_type=model_type, name=doc.name, path=doc.path, payload=codec.extract(model_type, d_path.read_text(encoding="utf-8")), semantic_tags=list(doc.semantic_tags))


def _load_doc(doc, root, model_type, m_entry, s_name, s_path, codec: StoreCodec = default_codec) -> RuntimeDocument | None:
    """One document, from the per-document cache when the default codec is in use."""
    if codec is not default_codec:
        return _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec)
    return cached_document(doc, root, s_path, s_name, m_entry.name, model_type, lambda: _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec))


def _resolve_model_type(resolver, model_ref: str, p_path, store_root: Path):
    """Resolve a model, trying the store's own project root before giving up.

    Linked stores register model_refs (e.g. ``docs.models:X``) that resolve
    relative to that store's repo root, not the caller's pythonpath. We try the
    caller path first, then the store root, and return None if neither works so a
    single unresolvable model does not abort a federated query.
    """
    for candidate in (p_path, str(store_root)):
        try:
            return resolver(model_ref, candidate)
        except Exception:  # noqa: BLE001 - graceful degradation across repos
            continue
    return None


def _load_one(s_path: Path, s_name: str, resolver, p_path, codec: StoreCodec = default_codec) -> list[RuntimeDocument]:
    root = project_root(s_path)
    docs = []
    for m in load_store_index(s_path).models:
        m_type = _resolve_model_type(resolver, m.model_ref, p_path, root)
        if m_type is None:
            continue
        d_idx = load_documents_index(root / load_models_index(root / m.models_index).documents_index)
        docs.extend([d for doc in d_idx.documents if (d := _load_doc(doc, root, m_type, m, s_name, s_path, codec))])
    return docs


def load_runtime_documents(store_path: Path, resolve_model_ref, pythonpath: str | None = None, include_linked: bool = False, codec: StoreCodec = default_codec) -> list[RuntimeDocument]:
    """The tracked documents of a store, extracted. With the default codec the load is cached
    by the state of the files it comes from (sldb.store.runtime_cache), so repeated queries
    do not read the store again. The list is fresh per call; the documents are shared."""
    def one(path: Path, name: str) -> list[RuntimeDocument]:
        loader = lambda: _load_one(path, name, resolve_model_ref, pythonpath, codec)  # noqa: E731
        return cached_store(path, name, pythonpath, loader) if codec is default_codec else loader()

    docs = list(one(store_path, "local"))
    if include_linked:
        for linked in load_store_index(store_path).stores:
            if store_exists(linked_store := _resolve_path(project_root(store_path), linked.path)):
                docs.extend(one(linked_store, linked.name))
    return docs


from sldb.store.query_engine.structural import (  # noqa: E402
    list_structural as list_structural,
    get_structural as get_structural,
)
from sldb.store.query_engine.structural_queries import (  # noqa: E402
    glob_structural as glob_structural,
    find_structural as find_structural,
)
from sldb.store.query_engine.semantic import (  # noqa: E402
    list_semantic as list_semantic,
    get_semantic as get_semantic,
    glob_semantic as glob_semantic,
    find_semantic as find_semantic,
)
from sldb.store.query_engine.global_semantic import (  # noqa: E402
    get_global_semantic as get_global_semantic,
    list_global_semantic as list_global_semantic,
)
