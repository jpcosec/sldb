"""The declared references of a store that name no document."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.edge_index.unresolved_reference import UnresolvedReference


def unresolved_references(store: str | Path | None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[UnresolvedReference]:
    """Every value of a declared reference or containment field that names no document.

    A value resolves as an export id (`Model:name`), as the path of a tracked document, or as
    `Model:value` for the one model the field allows that has it (`__reference_models__`,
    `__containment__`). What is left is reported here and never stored as an edge; a free
    reference field only reports export ids.

    Args:
        store: The store (path, alias, or None to discover it).
        include_linked: Also read the linked stores' documents, their ids qualified by name.
        exclude_tags: Leave out the documents carrying one of these tags.

    Returns:
        One record per unresolved value, in index order.
    """
    return list(load_edge_index(store, include_linked, exclude_tags).unresolved_references)
