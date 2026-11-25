"""What a tag reaches in the semantic DAG: itself, everything below it, and the equivalents."""

from __future__ import annotations

from typing import Any

from sldb.store.semantic_dag_graph import under


def tag_reach(dag: Any, tag: str) -> set[str]:
    """`tag`, every tag below it, and what is equivalent to any of those (to a fixpoint)."""
    found, todo = set(), [tag]
    while todo:
        t = todo.pop()
        if t not in found:
            found.add(t)
            todo += [*under(dag, t), *_equivalents(dag, t)]
    return found


def _equivalents(dag: Any, tag: str) -> set[str]:
    eq = dag.equivalences
    return {*eq.get(tag, []), *(k for k, v in eq.items() if tag in v)}
