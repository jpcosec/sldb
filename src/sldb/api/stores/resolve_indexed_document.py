"""Find a tracked document by `Model:name`, where Model may be a base of the document's model.

A document is tracked under its own model. Asking for it under a base model (`TaskDoc:task-x`
for a document tracked as `TaskCodeDoc:task-x`) finds it too: an instance of a submodel is an
instance of its bases, as the `extends` relation says. The answer comes from the store's indexes
alone (`base_models` of each model index, or of the owner's for an inherited model), so no model
class is imported.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.ambiguous_document import AmbiguousDocument
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.model_origin import owner_entry


def _bases(store_path: Path, entry, models_index) -> list[str]:
    """The model's bases; an inherited entry keeps them in its owner's model index."""
    if models_index.base_models or not entry.origin:
        return list(models_index.base_models)
    owned = owner_entry(store_path, entry)
    if owned is None:
        return []
    owner, owner_model = owned
    return list(load_models_index(project_root(owner) / owner_model.models_index).base_models)


def _family_hits(store_path: Path, model: str, name: str) -> list[dict[str, str]]:
    """`{name, model, path}` of `name` in `model` and in every model whose bases include it."""
    root, hits = project_root(store_path), []
    for entry in sorted(load_store_index(store_path).models, key=lambda item: item.name):
        models_index = load_models_index(root / entry.models_index)
        if entry.name != model and model not in _bases(store_path, entry, models_index):
            continue
        documents = load_documents_index(root / models_index.documents_index).documents
        hits += [{"name": d.name, "model": entry.name, "path": d.path} for d in documents if d.name == name]
    return hits


def resolve_indexed_document(store_path: Path, model: str, name: str) -> dict[str, str] | None:
    """`{name, model, path}` of the document `model:name`, or None when the store has none.

    An exact match on the model wins. Otherwise the document is looked up among the models whose
    `base_models` include `model`; the returned `model` is the one that tracks it.

    Args:
        store_path: The store's `.sldb` directory.
        model: The asked model name, the document's own model or one of its bases.
        name: The document name.

    Raises:
        AmbiguousDocument: no exact match and more than one submodel tracks `name`.
    """
    hits = _family_hits(store_path, model, name)
    exact = [hit for hit in hits if hit["model"] == model]
    if exact or len(hits) <= 1:
        return (exact or hits or [None])[0]
    raise AmbiguousDocument(model, name, [hit["model"] for hit in hits])


def indexed_model_bases(store_path: Path) -> dict[str, list[str]]:
    """Each tracked model's bases, nearest first, read from the store's indexes alone.

    A consumer that groups documents by model family (`model <= TaskDoc`) asks here instead of
    keeping its own list of submodels; an inherited model answers with its owner's bases.

    Args:
        store_path: The store's `.sldb` directory.

    Returns:
        `{model name: [base names]}`, an empty list for a model with no document bases.
    """
    root = project_root(store_path)
    return {
        entry.name: _bases(store_path, entry, load_models_index(root / entry.models_index))
        for entry in sorted(load_store_index(store_path).models, key=lambda item: item.name)
    }
