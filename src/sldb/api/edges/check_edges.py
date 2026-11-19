"""Validate every edge of a store's index against its relation type."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.acyclic import cycle_errors
from sldb.store.edge_index.federation import federated_stores
from sldb.store.edge_index.validation import untracked_builtins, validate_edge_index_by_store


def check_edges(store: str | Path | None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeCheckReport:
    """The cross-document validation of the edge index, as a report.

    Args:
        store: The store (path, alias, or None to discover it).
        include_linked: Validate the federated index, not just the local store's.
        exclude_tags: Leave out the documents carrying one of these tags before validating.

    Returns:
        The errors found (the same sentences TypedIngestError carried, plus a cycle in a
        relation that must be acyclic) and the stale documents, this store's apart from those
        only its linked stores' edges commit (`linked_errors`, `linked_stale`: not a failure here).
    """
    index = load_edge_index(store, include_linked, exclude_tags)
    links = _link_names(store) if include_linked else set()
    own, linked = validate_edge_index_by_store(index)
    linked_stale = [s for s in index.stale if _is_linked(s, links)]
    return EdgeCheckReport(errors=index.problems + own + cycle_errors(index), stale=[s for s in index.stale if s not in linked_stale],
                           untracked_builtins=untracked_builtins(index), linked_errors=linked, linked_stale=linked_stale)


def _link_names(store: str | Path | None) -> set[str]:
    """The names the linked stores (transitively) are linked under, which prefix their stale ids."""
    return {name for _, name in federated_stores(open_store(store, mode="readonly").store_path, True) if name is not None}


def _is_linked(stale_id: str, links: set[str]) -> bool:
    """A stale id is a linked store's when it starts `<link name>:Model:`: the owner is read from
    the link name, not from counting colons (a document name may carry them)."""
    head, _, rest = stale_id.partition(":")
    return head in links and ":" in rest
