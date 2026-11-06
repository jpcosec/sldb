"""Choosing tracked documents by selector: the one rule `sldb.api.select_documents`,
`glob_structural` and `find_structural` share (GD23, plan generalizar-desde-deskops).

Candidates come from the documents indexes alone (no model import, no extraction); `model`
reads each model index's `base_models` (an inherited entry, its owner's); `where` is evaluated
on the edge index's payload projection with the store's own evaluator (`findings` over
`index_view`). A linked store is read only when `include_linked` asks for every direct link,
or when the `ref` names that link explicitly (`alias:name`); links of links are never read.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.model_origin import owner_entry
from sldb.store.query_engine.document_selection_filters import keep_matching, prefix_tier

ROW_KEYS = ("export_id", "model", "name", "path")


def select_rows(
    store_path: Path, *, ref: tuple[str | None, str] | None = None, prefix: str | None = None,
    path_glob: str | None = None, model: str | None = None, where: str | None = None,
    include_linked: bool = False, expect: str = "many", model_type_of: Callable[..., Any] | None = None,
) -> list[dict[str, str]]:
    """`{export_id, model, name, path}` of the documents every given key keeps (a conjunction).

    Args:
        store_path: The store's `.sldb` directory.
        ref: `(link alias or None, reference)`: the reference names the document by name,
            tracked path, `Model/name` or `Model:name` inside that store.
        prefix: Name prefix. With `expect="one"` an exact name wins over the prefix matches.
        path_glob: Shell pattern over the path relative to the project root (`**` recursive).
        model: A model name; its whole family (the model and every model extending it) is kept.
        where: A predicate of `docs/architecture/rules-language.md` over the payload projection.
        include_linked: Also read every store linked directly to this one.
        expect: `"many"` (every match) or `"one"` (the prefix rule narrows to an exact name).
        model_type_of: `(model_ref, project_root) -> class | None` for the edge index composer.

    Returns:
        The local store's rows by path, then each linked store's (by alias, then path).
    """
    rows = candidates(store_path, include_linked, None if ref is None else ref[0])
    rows = keep_matching(store_path, rows, ref, path_glob, model, where, model_type_of)
    return [{key: row[key] for key in ROW_KEYS} for row in prefix_tier(rows, prefix, expect)]


def candidates(store_path: Path, include_linked: bool, alias: str | None) -> list[dict[str, Any]]:
    """Every tracked document of the store, then of its direct links (all of them, or `alias`)."""
    rows = store_rows(store_path, None)
    for path, name in linked_stores(store_path):
        if include_linked or name == alias:
            rows += store_rows(path, name)
    return rows


def linked_stores(store_path: Path) -> list[tuple[Path, str]]:
    """`(store path, alias)` of each direct link that is a store, by alias."""
    from sldb.store.query import _linked_stores

    return sorted(_linked_stores(store_path), key=lambda link: link[1])


def store_rows(store_path: Path, alias: str | None) -> list[dict[str, Any]]:
    """One store's documents by path; `export_id` carries `alias:` when the store is linked."""
    root, rows = project_root(store_path), []
    for entry in load_store_index(store_path).models:
        models_index = load_models_index(root / entry.models_index)
        bases = model_bases(store_path, entry, models_index)
        for doc in load_documents_index(root / models_index.documents_index).documents:
            export_id = f"{entry.name}:{doc.name}" if alias is None else f"{alias}:{entry.name}:{doc.name}"
            rows.append({"export_id": export_id, "model": entry.name, "name": doc.name, "path": doc.path, "bases": bases, "store": alias})
    return sorted(rows, key=lambda row: row["path"])


def model_bases(store_path: Path, entry: Any, models_index: Any) -> list[str]:
    """The model's bases, every one above it; an inherited entry keeps them in its owner's index."""
    if models_index.base_models or not entry.origin:
        return list(models_index.base_models)
    owned = owner_entry(store_path, entry)
    if owned is None:
        return []
    owner, owner_model = owned
    return list(load_models_index(project_root(owner) / owner_model.models_index).base_models)
