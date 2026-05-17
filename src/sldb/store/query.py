from __future__ import annotations

from pathlib import Path

from sldb.runtime.validation import extract_model_data
from sldb.store.layout import project_root, store_exists
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
)
from sldb.store.query_engine.models import RuntimeDocument


def _resolve_path(base: Path, maybe_relative: str) -> Path:
    """Resolves a potentially relative path against a base path."""
    path = Path(maybe_relative)
    return path if path.is_absolute() else (base / path).resolve()


def load_runtime_documents(
    store_path: Path,
    resolve_model_ref,
    pythonpath: str | None = None,
    include_linked: bool = False,
) -> list[RuntimeDocument]:
    """
    Loads tracked documents into memory for querying.
    """

    def _load_one(current_store_path: Path, store_name: str) -> list[RuntimeDocument]:
        root = project_root(current_store_path)
        store_index = load_store_index(current_store_path)
        runtime_docs: list[RuntimeDocument] = []
        for model_entry in store_index.models:
            model_type = resolve_model_ref(model_entry.model_ref, pythonpath)
            models_idx = load_models_index(root / model_entry.models_index)
            docs_idx = load_documents_index(root / models_idx.documents_index)
            for doc in docs_idx.documents:
                doc_path = root / doc.path
                if not doc_path.exists():
                    continue
                payload = extract_model_data(
                    model_type, doc_path.read_text(encoding="utf-8")
                )
                runtime_docs.append(
                    RuntimeDocument(
                        store_name=store_name,
                        store_path=current_store_path,
                        model_name=model_entry.name,
                        model_type=model_type,
                        name=doc.name,
                        path=doc.path,
                        payload=payload,
                        semantic_tags=list(doc.semantic_tags),
                    )
                )
        return runtime_docs

    docs = _load_one(store_path, "local")
    if include_linked:
        store_index = load_store_index(store_path)
        for linked in store_index.stores:
            linked_store = _resolve_path(project_root(store_path), linked.path)
            if store_exists(linked_store):
                docs.extend(_load_one(linked_store, linked.name))
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
