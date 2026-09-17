"""What the store itself contributes: its node, `has_model`, and the semantic DAG's edges."""

from __future__ import annotations

from sldb.store.edge_index.node_ids import STORE_NODE_ID, model_node_id, tag_node_id
from sldb.store.edge_index.records import edge, tag_nodes
from sldb.store.models import EdgeContribution, EdgeNodeRecord, SemanticDAG, StoreIndex


def build_store_edges(st_idx: StoreIndex, dag: SemanticDAG) -> EdgeContribution:
    """The store's shard. The store node carries no path and no `hash_a`: a shard must read the
    same wherever the project is checked out, and `hash_a` is already the store index's.

    Args:
        st_idx: The store index (its registered models).
        dag: The semantic DAG (tag parents and cross-store equivalences).

    Returns:
        The shard, not yet stamped with `edges_version`.
    """
    nodes = [EdgeNodeRecord(id=STORE_NODE_ID, node_type="sldb_store")] + tag_nodes(_dag_tags(dag))
    edges = [edge(STORE_NODE_ID, model_node_id(m.name), "has_model", "structural") for m in sorted(st_idx.models, key=lambda m: m.name)]
    for node in sorted(dag.nodes, key=lambda n: n.id):
        edges += [edge(tag_node_id(node.id), tag_node_id(p), "semantic_parent", "structural") for p in sorted(set(node.parents))]
    for tag, equivalents in sorted(dag.equivalences.items()):
        edges += [edge(tag_node_id(tag), tag_node_id(e), "semantic_equivalent", "structural") for e in sorted(set(equivalents))]
    return EdgeContribution(nodes=nodes, edges=edges)


def _dag_tags(dag: SemanticDAG) -> set[str]:
    tags = {n.id for n in dag.nodes}.union(*(n.parents for n in dag.nodes))
    return tags.union(dag.equivalences, *dag.equivalences.values())
