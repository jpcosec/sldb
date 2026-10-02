"""Resolve a `composes` edge's path target to the document node that owns that path.

A composition ref is a project path, and which document owns a path is something only the
whole index knows -- so, like the other rules that span documents, this runs when the index is
composed rather than in a shard. Paths are matched as the renderer resolves them: against the
project root, so `desk/tasks/task-a.md` and `./desk/tasks/task-a.md` are the same document.

A ref no document owns keeps no edge: the model declared a shape (`origin: "schema"`), not an
authored assertion, so `resolve_edges` drops it exactly as it drops a declared reference whose
target is not tracked.
"""

from __future__ import annotations

from posixpath import normpath

from sldb.store.edge_index.composition_edges import COMPOSES, UNRESOLVED_TARGET
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def resolve_composition_edges(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord]) -> list[EdgeRecord]:
    """Every edge, with each `composes` target rewritten from its path to a document node id."""
    owners = _owners_by_path(nodes)
    return [_resolved(e, owners) for e in edges]


def _resolved(edge: EdgeRecord, owners: dict[str, str]) -> EdgeRecord:
    """The edge pointing at the document that owns its `ref_path`, or left unresolved to be dropped."""
    if edge.relation != COMPOSES or not edge.target.startswith(UNRESOLVED_TARGET):
        return edge
    owner = owners.get(_normalized(edge.metadata.get("ref_path", "")))
    if owner is None:
        return edge
    return EdgeRecord(source=edge.source, target=owner, relation=edge.relation, metadata=edge.metadata)


def _owners_by_path(nodes: dict[str, EdgeNodeRecord]) -> dict[str, str]:
    """Project-relative path -> node id of the document tracked at it.

    A linked store's documents are left out: its paths are relative to its own root, so the
    same path can name a document in each store and a ref means the composing store's one.
    """
    owners: dict[str, str] = {}
    for node in nodes.values():
        path = node.semantics.get("path") if "export_id" in node.semantics else None
        if path and not node.semantics.get("store"):
            owners.setdefault(_normalized(str(path)), node.id)
    return owners


def _normalized(path: str) -> str:
    """A ref and a tracked path compared the way the renderer resolves them, under the root."""
    return normpath(path.strip().strip("`").replace("\\", "/")).lstrip("/")
