"""The project's own sldb store, as a project graph reads it."""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.tracked_documents import tracked_documents
from sldb.store.edge_index.edge_index import EdgeIndex


class ProjectStore(NamedTuple):
    """The store's composed edge index (its own shards only) and the documents it tracks."""

    index: EdgeIndex
    tracked: dict[str, DocRefStatus]


def load_project_store(root: Path, document_paths: list[str]) -> ProjectStore | None:
    """The store at `root/.sldb`, or None when the project has none.

    Args:
        root: The project root.
        document_paths: Repo-relative paths of the document nodes, looked up as tracked.

    Returns:
        The cached composed index of the store alone (linked stores are not read) and
        `{path: status}` of the tracked documents.
    """
    store = root / ".sldb"
    if not (store / "core" / "store_index.yaml").is_file():
        return None
    return ProjectStore(index=load_edge_index(store, include_linked=False), tracked=tracked_documents(store, document_paths))
