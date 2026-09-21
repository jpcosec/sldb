"""Declaring that one tag is a kind of another, beyond what its dotted name already says.

A tag's name gives it one parent: `type.knowledge.spec` hangs from `type.knowledge` because of
the dots. That is the only way a tag has ever got a parent. The DAG file can hold more — and
since `se.` walks the DAG's edges, a parent written there is read — but nothing wrote it. These
do, with the two guards a DAG needs: no cycles, and no removing what the name will put back.
"""

from __future__ import annotations

from pathlib import Path

from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_semantic_dag, save_semantic_dag
from sldb.store.models.semantic_node import SemanticNode
from sldb.store.semantic_dag_graph import above


def add_semantic_parent(store_path: Path, tag: str, parent: str) -> bool:
    """Declare `tag` a kind of `parent`; False when it already was."""
    dag = load_semantic_dag(store_path)
    node, known = _node(dag, tag), {n.id for n in dag.nodes}
    _refuse_unknown(parent, known)
    _refuse_cycle(dag, tag, parent)
    if parent in node.parents:
        return False
    node.parents = sorted({*node.parents, parent})
    save_semantic_dag(store_path, dag)
    return True


def remove_semantic_parent(store_path: Path, tag: str, parent: str) -> bool:
    """Undeclare it; False when it was not declared. A parent the name implies cannot go."""
    dag = load_semantic_dag(store_path)
    node = _node(dag, tag)
    if _implied_by_name(tag, parent):
        raise SLDBStoreError(f"'{parent}' is the parent '{tag}' gets from its own name; rename the tag to change it.")
    if parent not in node.parents:
        return False
    node.parents = [p for p in node.parents if p != parent]
    save_semantic_dag(store_path, dag)
    return True


def _node(dag, tag: str) -> SemanticNode:
    for node in dag.nodes:
        if node.id == tag:
            return node
    raise SLDBStoreError(f"Unknown semantic tag '{tag}': no document or model carries it.")


def _refuse_unknown(tag: str, known: set[str]) -> None:
    if tag not in known:
        raise SLDBStoreError(f"Unknown semantic tag '{tag}': no document or model carries it.")


def _refuse_cycle(dag, tag: str, parent: str) -> None:
    if parent == tag:
        raise SLDBStoreError(f"'{tag}' cannot be a kind of itself.")
    if tag in above(dag, parent):
        raise SLDBStoreError(f"'{tag}' cannot be a kind of '{parent}': '{parent}' is already a kind of '{tag}'.")


def _implied_by_name(tag: str, parent: str) -> bool:
    return tag.startswith(f"{parent}.") and "." not in tag[len(parent) + 1 :]
