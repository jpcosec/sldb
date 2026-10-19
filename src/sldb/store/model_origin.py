"""Where an inherited model comes from: the linked store that owns it.

A model is defined once, in the store that owns it. Another store that tracks documents of
that model registers an *inherited* entry (`ModelEntry.origin` = the alias it links the owner
under) instead of a copy: no source path of its own, and the class imports from the owner's
project root. What stays local is what belongs to the store: the roster of its own documents
and the contract it last signed, so the store keeps working while the owner is away.

The graph already treats a model as one node across stores (`qualify_id` leaves model ids
unqualified); this is the registry agreeing with it.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from sldb.store.io import load_store_index
from sldb.store.layout import project_root, store_exists
from sldb.store.model_import_root import import_root


def linked_store(store_path: Path, alias: str) -> Path | None:
    """The existing store this store links under `alias`, if any."""
    root = project_root(store_path)
    link = next((s for s in load_store_index(store_path).stores if s.name == alias), None)
    if link is None:
        return None
    candidate = Path(link.path) if Path(link.path).is_absolute() else root / link.path
    return candidate.resolve() if store_exists(candidate) else None


def owner_entry(store_path: Path, entry: Any) -> tuple[Path, Any] | None:
    """(owner store, the owner's entry) of an inherited entry; None when the owner is
    unreachable or no longer registers the model."""
    owner = linked_store(store_path, entry.origin) if entry.origin else None
    if owner is None:
        return None
    found = next((m for m in load_store_index(owner).models if m.name == entry.name and not m.origin), None)
    return (owner, found) if found is not None else None


def owner_import_roots(store_path: Path) -> list[Path]:
    """The directories the store's inherited models import from (the owner's package root),
    once each, in entry order."""
    roots: list[Path] = []
    for entry in load_store_index(store_path).models:
        found = owner_entry(store_path, entry)
        root = import_root(project_root(found[0]), found[1].model_ref, found[1].path) if found else None
        if root is not None and root not in roots:
            roots.append(root)
    return roots


def add_owner_import_roots(store_path: Path) -> None:
    """Put the owners' project roots on `sys.path`, once each, so inherited models import
    without a `--pythonpath`; a path given explicitly is inserted in front of them later."""
    for root in reversed([str(r.resolve()) for r in owner_import_roots(store_path)]):
        if root not in sys.path:
            sys.path.insert(0, root)


def shadowed_models(store_path: Path, same_class=lambda a, b: a == b) -> list[dict[str, Any]]:
    """Models this store owns under a name a linked store also owns.

    The graph has one node per model name, so two classes behind one name merge there. A
    copy (the same class, compared by `same_class`; by reference string unless the caller can
    import) can become inherited; a different class is an override that
    should extend the owner's under a name of its own. Reported, never refused; sldb's own
    models are left out.
    """
    idx = load_store_index(store_path)
    return [found for link in idx.stores for found in _shadowed_by(store_path, idx, link.name, same_class)]


def _shadowed_by(store_path: Path, idx: Any, alias: str, same_class) -> list[dict[str, Any]]:
    """The models this store owns that the store linked as `alias` owns too."""
    other = linked_store(store_path, alias)
    if other is None:
        return []
    theirs = {m.name: m for m in load_store_index(other).models if not m.origin}
    return [{"model": m.name, "store": alias, "copy": same_class(m.model_ref, theirs[m.name].model_ref)} for m in idx.models if not m.origin and m.name in theirs and not _builtin(m)]


def _builtin(entry: Any) -> bool:
    """sldb's own models (RelationDoc, ...) are the library's vocabulary: every store may
    register them, and no store owns them."""
    return entry.model_ref.startswith("sldb.")
