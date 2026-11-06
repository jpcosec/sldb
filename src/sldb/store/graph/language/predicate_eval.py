"""Evaluate a parsed predicate on one element of a graph view: `(value, clause, seen)`.

An element is a node of the view (`id`, `model`, `base_models`, `payload`, `name`) or an
incomplete one (`{"id", "incomplete"}`), on which every predicate is `incomplete` (§3).
`ctx` carries the view (paths read it) and the subject's `{field}` values.
"""

from __future__ import annotations

from sldb.store.graph.language.predicate_explain import counted, junction, quantified
from sldb.store.graph.language.predicate_leaves import leaf_value
from sldb.store.graph.language.predicate_paths import reach


def evaluate(node: tuple, item: dict, ctx: dict) -> tuple:
    """`(True | False | None, clause, seen)` for one tree node on one element."""
    if item.get("incomplete"):
        return None, node[1], {"incomplete": item["incomplete"]}
    return _EVALUATORS[node[0]](node, item, ctx)


def _leaf(node: tuple, item: dict, ctx: dict) -> tuple:
    holds, seen = leaf_value(node[2], node[3], item, ctx)
    return holds, node[1], seen


def _not(node: tuple, item: dict, ctx: dict) -> tuple:
    value, _, seen = evaluate(node[2], item, ctx)
    return (None if value is None else not value), node[1], seen


def _junction(node: tuple, item: dict, ctx: dict) -> tuple:
    left = evaluate(node[2], item, ctx)
    return junction(node[0], node[1], left, lambda: evaluate(node[3], item, ctx))


def _quant(node: tuple, item: dict, ctx: dict) -> tuple:
    results = [evaluate(node[4], element, ctx) for element in reach(ctx["view"], item, node[3])]
    return quantified(node[2], node[1], results)


def _count(node: tuple, item: dict, ctx: dict) -> tuple:
    results = [evaluate(node[3], element, ctx) for element in reach(ctx["view"], item, node[2])]
    return counted(node, item, ctx, results)


_EVALUATORS = {"leaf": _leaf, "not": _not, "and": _junction, "or": _junction, "quant": _quant, "count": _count}
