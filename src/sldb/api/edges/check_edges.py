"""Validate every edge of a store's index against its relation type."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.edge_index.acyclic import cycle_errors
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
    own, linked = validate_edge_index_by_store(index)
    linked_stale = [s for s in index.stale if s.count(":") == 2]
    return EdgeCheckReport(errors=index.problems + own + cycle_errors(index), stale=[s for s in index.stale if s not in linked_stale],
                           untracked_builtins=untracked_builtins(index), linked_errors=linked, linked_stale=linked_stale)
