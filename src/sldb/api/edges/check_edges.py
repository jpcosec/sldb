"""Validate every edge of a store's index against its relation type."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.edge_index.validation import validate_edge_index


def check_edges(store: str | Path | None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeCheckReport:
    """The cross-document validation kgdb's typed ingest did, as a report.

    Args:
        store: The store (path, alias, or None to discover it).
        include_linked: Validate the federated index, not just the local store's.
        exclude_tags: Leave out the documents carrying one of these tags before validating.

    Returns:
        The errors found (the same sentences TypedIngestError carried) and the stale documents.
    """
    index = load_edge_index(store, include_linked, exclude_tags)
    return EdgeCheckReport(errors=index.problems + validate_edge_index(index), stale=index.stale)
