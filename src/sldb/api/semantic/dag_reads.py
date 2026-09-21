"""One tag, as the DAG sees it: what it hangs from, what hangs from it, what it maps to."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_semantic_dag
from sldb.store.semantic_dag_graph import above, children, under


def semantic_tag(store: str | Path | None, tag: str) -> dict:
    """The tag's parents, children, everything above and below it, and its equivalents.

    Raises:
        SLDBStoreError: When no document or model carries the tag.
    """
    dag = load_semantic_dag(open_store(store).store_path)
    parents = _parents_of(dag, tag)
    below = {"children": children(dag, tag), "below": under(dag, tag)}
    return {"tag": tag, "parents": parents, **below, "above": above(dag, tag), "equivalents": sorted(dag.equivalences.get(tag, []))}


def _parents_of(dag, tag: str) -> list[str]:
    node = next((n for n in dag.nodes if n.id == tag), None)
    if node is None:
        raise SLDBStoreError(f"Unknown semantic tag '{tag}': no document or model carries it.")
    return sorted(node.parents)
