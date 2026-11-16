"""The `ViewDoc` nodes of a store and of every store it links to (H9), read from the ViewDoc
edges shards alone: listing the views never composes the federated edge index (which, through
transitive links, can be every store of the machine)."""

from __future__ import annotations

from pathlib import Path

from sldb.api.views.view_source import VIEW_MODEL
from sldb.store.edge_index.federation import federated_stores, qualify
from sldb.store.io.shard_compose import compose_edges_documents
from sldb.store.models import EdgeNodeRecord


def view_nodes(store_path: Path) -> list[EdgeNodeRecord]:
    """The ViewDoc nodes, local and linked (transitively), qualified and stamped with
    `facets.source.store_path` as the composed index has them; the first contributor of an id wins."""
    nodes: dict[str, EdgeNodeRecord] = {}
    for path, name in federated_stores(Path(store_path), True):
        for shard in compose_edges_documents(path, VIEW_MODEL, copy=False):
            for node in qualify(shard, name).nodes:
                if node.node_type == VIEW_MODEL and node.id not in nodes:
                    nodes[node.id] = _stamped(node, path)
    return sorted(nodes.values(), key=lambda n: n.id)


def _stamped(node: EdgeNodeRecord, store_path: Path) -> EdgeNodeRecord:
    return node.model_copy(update={"facets": {**node.facets, "source": {"store_path": str(store_path)}}})
