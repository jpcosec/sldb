"""`sldb.api.referrers(store, target)` (GD22): the incoming references of a document or of a
project graph node (docs/architecture/references.md).

The declared fields of tracked documents (a scalar value or an element of a list, `origin:
schema`) come from the store's composed edge index, the one every sldb write keeps current;
the mentions a `MentionPattern` captures in prose (`origin: mention`, located `path:line`) come
from `ProjectGraph.edges_to` of GD21, memoized per process. Neither reads walk the project.

`target` is resolved first as a tracked document, with the rule of `doc_status` plus the
export id form (`name`, `Model/name`, `Model:name` or a tracked path; several candidates are an
error naming them), then as a project graph node id (`kind:identity`); anything else is
`SLDBDocumentTargetError`. A document that is also a project node (its path is on a surface)
has both kinds of referrers.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.store_project_graph import project_graph
from sldb.api.edges.referrer import Referrer
from sldb.api.edges.rewrite_mentions import mention_hits
from sldb.api.edges.rewrite_values import schema_hits
from sldb.api.stores.doc_ref import matches_doc_ref
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBStoreError

Hit = tuple[Referrer, str | None]


class Target(NamedTuple):
    """What a target (or a replacement) resolved to: a tracked document, a project node, or neither."""

    given: str
    model: str | None
    name: str | None
    path: str | None
    node_id: str | None

    @property
    def export_id(self) -> str | None:
        """`Model:name` when the target is a tracked document."""
        return f"{self.model}:{self.name}" if self.model else None


def referrers(store: str | Path | None, target: str, pythonpath: str | None = None) -> list[Referrer]:
    """Every reference to `target`, fields first (by source, field and position), then mentions (by path and line).

    Args:
        store: The store (path, alias, or None to discover it).
        target: A tracked document (`name`, `Model/name`, `Model:name`, tracked path) or a project node id.
        pythonpath: Unused by the read; accepted so callers pass what they pass `rewrite_references`.

    Raises:
        SLDBDocumentTargetError: `target` names no document and no project node, or several documents.
    """
    location = open_store(store, mode="readonly")
    graph = optional_graph(location.store_path)
    return [referrer for referrer, _ in find_hits(location, resolve_target(location, graph, target), graph)]


def resolve_target(location: StoreLocation, graph: ProjectGraph | None, given: str) -> Target:
    """A tracked document first, then a project node id; else `SLDBDocumentTargetError`."""
    found = matching_documents(location.store_path, given)
    if len(found) > 1:
        candidates = ", ".join(f"{d['model']}:{d['name']}" for d in found)
        raise SLDBDocumentTargetError(f"Ambiguous document target: {given} (candidates: {candidates})")
    if found:
        document = found[0]
        return Target(given, document["model"], document["name"], document["path"], node_id_of_path(graph, document["path"]))
    if graph is not None and given in graph.nodes.lookup.by_id:
        return Target(given, None, None, None, given)
    raise SLDBDocumentTargetError(f"Unknown document target: {given}")


def matching_documents(store_path: Path, ref: str) -> list[dict[str, str]]:
    """The tracked documents `ref` names by name, `Model/name`, `Model:name` or tracked path."""
    ref = ref.strip().strip("/")
    return [d for d in indexed_documents(store_path) if matches_doc_ref(ref, d["name"], d["path"], d["model"]) or ref == f"{d['model']}:{d['name']}"]


def optional_graph(store_path: Path) -> ProjectGraph | None:
    """The declared project graph, or None when the store declares none (then there are no mentions)."""
    try:
        return project_graph(store_path)
    except (SLDBStoreError, FileNotFoundError):
        return None


def node_id_of_path(graph: ProjectGraph | None, path: str) -> str | None:
    """The project node whose file is `path`, when the graph has one."""
    node = graph.nodes.lookup.by_path.get(path) if graph is not None else None
    return node.id if node is not None else None


def find_hits(location: StoreLocation, target: Target, graph: ProjectGraph | None) -> list[Hit]:
    """Field hits (with the value as written) then mention hits (value found when rewriting)."""
    hits = schema_hits(location.store_path, target.export_id) if target.export_id else []
    if graph is not None and target.node_id:
        hits += mention_hits(graph, target.node_id)
    return hits
