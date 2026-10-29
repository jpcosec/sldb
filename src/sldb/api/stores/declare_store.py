"""The declaration a store's current index implies: the starting `.sldb/store.yaml`.

Run once per store to move it to a declared layout; after that the file is edited by hand (or
by the commands that register models and links) and the index is what gets rebuilt from it.
Generators cannot be read off an index, so an existing declaration's are kept, and so are its
authored `include` rules (a glob is never flattened into the paths it matches): only what they
do not cover is added.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.declared_includes import declared_includes
from sldb.api.stores.merged_includes import merged_includes
from sldb.api.stores.store_declaration import StoreDeclaration, declaration_path, load_declaration
from sldb.store.io import load_store_index


def declare_store(store_path: Path, root: Path) -> StoreDeclaration:
    """Links, models, predicates and include rules that reproduce the store as it is now."""
    index = load_store_index(store_path)
    return StoreDeclaration(
        links=[{"name": link.name, "path": link.path} for link in index.stores],
        models=[_model(entry, root) for entry in index.models],
        predicates={p.name: {"axis": p.axis, "description": p.description} for p in sorted(index.predicates, key=lambda p: p.name)},
        **_kept(store_path),
        include=_include(store_path, root),
    )


def _include(store_path: Path, root: Path) -> list[dict]:
    """The authored rules of an existing declaration, kept as they are and completed; the
    rules derived from the index only for a store that has no declaration yet."""
    if not declaration_path(store_path).is_file():
        return declared_includes(store_path, root)
    return merged_includes(store_path, root, load_declaration(store_path).include)


def _model(entry, root: Path) -> dict:
    declared = {"name": entry.name, "model_ref": entry.model_ref}
    if entry.origin:
        declared["origin"] = entry.origin
    elif _inside(root, entry.path):
        declared["path"] = Path(entry.path).as_posix()
    if entry.canonical:
        declared["canonical"] = True
    return declared


def _kept(store_path: Path) -> dict:
    """What an index cannot say: the generators and the paths they write, from the current file."""
    if not declaration_path(store_path).is_file():
        return {}
    current = load_declaration(store_path)
    return {"generate": current.generate, "derived": current.derived}


def _inside(root: Path, path: str) -> bool:
    """A model source the project holds. One outside it (sldb's own models, from the installed
    package) is declared by `model_ref` alone: its absolute path would pin one checkout."""
    if not path:
        return False
    source = Path(path) if Path(path).is_absolute() else root / path
    return source.resolve().is_relative_to(root.resolve()) and not Path(path).is_absolute()
