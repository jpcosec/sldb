"""The semantic DAG (tag prefixes and equivalences), grown incrementally (PLAN 15 capa 5):
bounded by the store's tag vocabulary, not its document count, so it stays one small file —
re-saved only when a document actually introduced a tag or prefix it did not already have."""

from __future__ import annotations

from sldb.store.io import load_semantic_dag, save_semantic_dag
from sldb.store.models import SemanticDAG, SemanticNode
from sldb.store.semantic_tags import _prefix_edges


def sync_semantic_dag(store_path, tags: set[str]) -> None:
    if not tags:
        return
    dag = load_semantic_dag(store_path)
    parents = {n.id: set(n.parents) for n in dag.nodes}
    known = set(parents)
    changed = any([_add_tag(tag, known, parents) for tag in tags])
    if changed:
        _save_dag(store_path, parents, dag.equivalences)


def _add_tag(tag: str, known: set, parents: dict) -> bool:
    changed = _add_node(tag, known, parents)
    for parent, child in _prefix_edges(tag):
        changed = _add_edge(parent, child, known, parents) or changed
    return changed


def _add_node(node_id: str, known: set, parents: dict) -> bool:
    if node_id in known:
        return False
    known.add(node_id)
    parents.setdefault(node_id, set())
    return True


def _add_edge(parent: str, child: str, known: set, parents: dict) -> bool:
    changed = _add_node(child, known, parents)
    changed = _add_node(parent, known, parents) or changed
    if parent not in parents[child]:
        parents[child].add(parent)
        changed = True
    return changed


def _save_dag(store_path, parents: dict, equivalences: dict) -> None:
    nodes = [SemanticNode(id=n_id, parents=sorted(p)) for n_id, p in sorted(parents.items())]
    save_semantic_dag(store_path, SemanticDAG(nodes=nodes, equivalences=equivalences))
