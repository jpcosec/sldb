"""The declaration a store's current index implies: the starting `.sldb/store.yaml`.

Run once per store to move it to a declared layout; after that the file is edited by hand (or
by the commands that register models and links) and the index is what gets rebuilt from it.
Generators cannot be read off an index, so an existing declaration's are kept.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.declared_includes import declared_includes
from sldb.api.stores.store_declaration import StoreDeclaration, declaration_path, load_declaration
from sldb.store.io import load_store_index


def declare_store(store_path: Path, root: Path) -> StoreDeclaration:
    """Links, models, predicates and include rules that reproduce the store as it is now."""
    index = load_store_index(store_path)
    return StoreDeclaration(
        links=[{"name": link.name, "path": link.path} for link in index.stores],
        models=[_model(entry) for entry in index.models],
        predicates={p.name: {"axis": p.axis, "description": p.description} for p in sorted(index.predicates, key=lambda p: p.name)},
        **_kept(store_path),
        include=declared_includes(store_path, root),
    )


def _model(entry) -> dict:
    declared = {"name": entry.name, "model_ref": entry.model_ref}
    if entry.origin:
        declared["origin"] = entry.origin
    elif entry.path:
        declared["path"] = entry.path
    if entry.canonical:
        declared["canonical"] = True
    return declared


def _kept(store_path: Path) -> dict:
    """What an index cannot say: the generators and the paths they write, from the current file."""
    if not declaration_path(store_path).is_file():
        return {}
    current = load_declaration(store_path)
    return {"generate": current.generate, "derived": current.derived}
