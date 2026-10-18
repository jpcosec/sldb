"""What the store itself contributes: its node, `has_model`, `links_to` the stores it links, and
the semantic DAG's edges."""

from __future__ import annotations

from sldb.store.edge_index.node_ids import STORE_NODE_ID, model_node_id, tag_node_id
from sldb.store.edge_index.records import edge, tag_nodes
from sldb.store.models import EdgeContribution, EdgeNodeRecord, SemanticDAG, StoreIndex


def build_store_edges(st_idx: StoreIndex, dag: SemanticDAG) -> EdgeContribution:
    """The store's shard. The store node carries no path and no `store_hash`: a shard must read the
    same wherever the project is checked out, and `store_hash` is already the store index's.

    Args:
        st_idx: The store index (its registered models).
        dag: The semantic DAG (tag parents and cross-store equivalences).

    Returns:
        The shard, not yet stamped with `edges_version`.
    """
    nodes = [EdgeNodeRecord(id=STORE_NODE_ID, node_type="sldb_store")] + tag_nodes(_dag_tags(dag))
    nodes += [EdgeNodeRecord(id=f"{STORE_NODE_ID}/{s.name}", node_type="sldb_store") for s in sorted(st_idx.stores, key=lambda s: s.name)]
    edges = [_has_model(m) for m in sorted(st_idx.models, key=lambda m: m.name)]
    edges += [edge(STORE_NODE_ID, f"{STORE_NODE_ID}/{s.name}", "links_to", "structural") for s in sorted(st_idx.stores, key=lambda s: s.name)]
    for node in sorted(dag.nodes, key=lambda n: n.id):
        edges += [edge(tag_node_id(node.id), tag_node_id(p), "semantic_parent", "structural") for p in sorted(set(node.parents))]
    for tag, equivalents in sorted(dag.equivalences.items()):
        edges += [edge(tag_node_id(tag), tag_node_id(e), "semantic_equivalent", "structural") for e in sorted(set(equivalents))]
    return EdgeContribution(nodes=nodes, edges=edges)


def _has_model(m):
    """`has_model`, naming the linked store an inherited model comes from (sldb.store.model_origin)."""
    if m.origin:
        return edge(STORE_NODE_ID, model_node_id(m.name), "has_model", "structural", origin_store=m.origin)
    return edge(STORE_NODE_ID, model_node_id(m.name), "has_model", "structural")


def _dag_tags(dag: SemanticDAG) -> set[str]:
    tags = {n.id for n in dag.nodes}.union(*(n.parents for n in dag.nodes))
    return tags.union(dag.equivalences, *dag.equivalences.values())
