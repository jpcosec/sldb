"""Whether a view needs the linked stores' documents (H11): `run_view` composes the edge index of
the calling store alone, and widens it to the linked stores only when something it evaluates
can name one. A section can when its selector says `include_linked`, or a `ref` or `prefix`
behind a link's alias; and a section with `edges` or `transitions` can when a reference of the
calling store's own documents names a linked one (the local index reports it unresolved)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.doc_ref import qualifier, split_doc_ref
from sldb.api.stores.store_links import find_link
from sldb.api.views.view_rows import substituted


def view_needs_linked(store_path: Path, view: Any, values: dict[str, str], index: Any) -> bool:
    """True when a section of `view` (its params filled by `values`) can reach a linked
    store's document; `index` is the calling store's own index."""
    if any(selects_linked(store_path, substituted(s.select, values)) for s in view.sections):
        return True
    return any(s.edges or s.transitions for s in view.sections) and reaches_links(store_path, index)


def selects_linked(store_path: Path, select: dict[str, Any]) -> bool:
    if select.get("include_linked") in (True, "true", "True"):
        return True
    return any(isinstance(select.get(key), str) and split_doc_ref(store_path, select[key])[0] is not None for key in ("ref", "prefix"))


def reaches_links(store_path: Path, index: Any) -> bool:
    """Whether a reference of the calling store's documents names a document behind a link alias."""
    named = {qualifier(u.target_export_id or u.target) for u in index.unresolved_references}
    return any(name and find_link(store_path, name) for name in named)
