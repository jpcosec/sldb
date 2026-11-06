"""Closures and the witness of a rule's finding (GO08 p3, rules.md §9).

The only facts a rule derives are the sets a closure `+` reaches: the language does not read
other rules' results. GO05's evaluator already computes them semi-naively
(`predicate_reach._closure`): each round expands only the elements new in the last one, an
element already seen is never expanded again, so it ends on a cycle; the sets live in memory
for one evaluation and are never stored. GO08 reuses it.

`witness` names the element behind a false (or incomplete) top-level quantifier, over that same
reach, with what it read: the first that falsifies an `all`, satisfies a `none`'s inner `any`,
or, for a false `any` (which the language explains with `seen: {}`, rules-language.md H16), the
first reached, since each one falsifies it; for an incomplete one, the first incomplete. The
finding's `seen` keeps the language's field -> value map (§4); the witness goes in its `what`.
"""

from __future__ import annotations

from typing import Any

from sldb.store.graph.language.predicate_ast import children, substitutions
from sldb.store.graph.language.predicate_eval import evaluate
from sldb.store.graph.language.predicate_parser import parse_predicate
from sldb.store.graph.language.predicate_paths import reach

_WANTED = {"all": False, "any": False, "none": True}


def witness(graph: Any, predicate: str, found: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    """`(export id, seen)` of the element behind `found` (an eval finding of `predicate`), or None."""
    root = parse_predicate(predicate).root
    quant = _top_quantifier(root, found["clause"]) if found["holds"] != "true" else None
    if quant is None:
        return None
    view, item = graph.located(found["node"])
    ctx = {"view": view, "subst": {name: item["payload"].get(name) for name in substitutions(root)}}
    wanted = None if found["holds"] == "incomplete" else _WANTED[quant[2]]
    results = ((element["id"], evaluate(quant[4], element, ctx)) for element in reach(view, item, quant[3]))
    return next(((node, result[2]) for node, result in results if result[0] is wanted), None)


def _top_quantifier(node: tuple, clause: str) -> tuple | None:
    """The quantifier whose text is `clause`, outside every other quantifier's body."""
    if node[0] in ("quant", "count"):
        return node if node[0] == "quant" and node[1] == clause else None
    return next((q for child in children(node) if (q := _top_quantifier(child, clause)) is not None), None)
