"""Make a store match its declaration: links, models, predicates, then the tracked files.

Idempotent: what is already registered or tracked is left alone, so a rebuild of a current
store writes nothing new. What the store has and the declaration does not is reported, never
removed: a declaration is not a license to delete authored state.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_registry.add_model import add_model
from sldb.api.model_registry.inherit_model import inherit_model
from sldb.api.stores.declared_files import declared_files
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.link_store import link_store
from sldb.api.stores.store_declaration import StoreDeclaration
from sldb.api.documents.track_document_file import track_document_file
from sldb.store.io import load_store_index, save_store_index
from sldb.store.model_import_root import import_root
from sldb.store.models import PredicateEntry


def apply_links(store_path: Path, root: Path, declaration: StoreDeclaration) -> list[str]:
    """Link each declared store that is not linked yet, or re-point one that moved."""
    current = {s.name: s.path for s in load_store_index(store_path).stores}
    changed = [link for link in declaration.links if current.get(link["name"]) != link["path"]]
    for link in changed:
        link_store(store_path, root / link["path"], link["name"], replace=link["name"] in current)
    return [link["name"] for link in changed]


def apply_models(store_path: Path, root: Path, declaration: StoreDeclaration) -> list[str]:
    """Register the declared models that are missing: local ones first, then the inherited."""
    registered = {m.name for m in load_store_index(store_path).models}
    missing = sorted((m for m in declaration.models if m["name"] not in registered), key=lambda m: bool(m.get("origin")))
    for model in missing:
        if model.get("origin"):
            inherit_model(store_path, f"{model['origin']}:{model['name']}")
        else:
            pythonpath = str(import_root(root, model["model_ref"], model.get("path", "")))
            add_model(store_path, model["model_ref"], pythonpath, canonical=bool(model.get("canonical")))
    return [m["name"] for m in missing]


def apply_predicates(store_path: Path, declaration: StoreDeclaration) -> bool:
    """Set the store's predicates to exactly the declared ones; True when they changed."""
    index = load_store_index(store_path)
    wanted = [PredicateEntry(name=n, axis=v["axis"], description=v.get("description", "")) for n, v in declaration.predicates.items()]
    if sorted(index.predicates, key=lambda p: p.name) == sorted(wanted, key=lambda p: p.name):
        return False
    save_store_index(store_path, index.model_copy(update={"predicates": wanted}))
    return True


def apply_includes(store_path: Path, root: Path, declaration: StoreDeclaration) -> list[str]:
    """Track every declared file that is not tracked yet under its declared model and name."""
    tracked = set(tracked_rows(store_path, root))
    new = [row for row in declared_files(root, declaration) if row not in tracked and (root / row[1]).is_file()]
    for model, path, name in new:
        track_document_file(store_path, model, root / path, name, str(root), force=True)
    return [path for _, path, _ in new]


def undeclared(store_path: Path, root: Path, declaration: StoreDeclaration) -> list[str]:
    """Tracked documents no include rule names: the declaration is missing them."""
    wanted = set(declared_files(root, declaration))
    return sorted(path for model, path, name in tracked_rows(store_path, root) if (model, path, name) not in wanted)


def missing_declared(root: Path, declaration: StoreDeclaration) -> list[str]:
    """Declared paths with no file: the declaration names something gone, and a build that
    tracked around it silently would rebuild a different store."""
    return sorted({path for _, path, _ in declared_files(root, declaration) if not (root / path).is_file()})
