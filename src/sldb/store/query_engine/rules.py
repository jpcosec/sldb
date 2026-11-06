"""The rules language as the spec tests call it (rules-language.md §8, H1; GO05 p7).

A thin facade over `sldb.store.graph.language`: `parse_predicate(text)`, `eval_predicate(
predicate, graph, subject=None)` over the test graph dict (H2) and `contract_hash(model,
field_hashes)` (§5). No logic of its own.
"""

from __future__ import annotations

from typing import Any

from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.graph.language.predicate_api import findings
from sldb.store.graph.language.predicate_parser import parse_predicate
from sldb.store.graph.language.predicate_view import graph_view


def eval_predicate(predicate: Any, graph: dict, subject: str | None = None) -> list[dict[str, Any]]:
    """`eval(predicate, subject)` over `{nodes: {...}, edges: [...]}`: a list of findings."""
    return findings(predicate, graph_view(graph), subject)


__all__ = ["contract_hash", "eval_predicate", "parse_predicate"]
