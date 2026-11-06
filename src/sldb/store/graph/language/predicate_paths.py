"""Paths (rules-language.md §2): parsing the steps, and reaching elements over a graph view.

A step is `field` (the `references` edges that field declares), `rel:<type>` (edges of that
relation type) or either prefixed by `^` (the inverse). A trailing `+` is the transitive
closure: repeated in the same direction, origin excluded, no duplicates, terminating on
cycles. Steps join with `.` (H5); a dotted name is that many field steps.
"""

from __future__ import annotations

from sldb.store.graph.language.predicate_cursor import expect_ident, is_op, peek, take
from sldb.store.graph.language.predicate_reach import reach_step


def parse_path(cur: list) -> tuple:
    """Steps up to the `:` that opens the quantified predicate."""
    steps = list(_step_group(cur))
    while is_op(cur, "."):
        take(cur)
        steps += _step_group(cur)
    return tuple(steps)


def _step_group(cur: list) -> list[tuple]:
    inverse = is_op(cur, "^") and take(cur) is not None
    steps = [(kind, name, False, False) for kind, name in _names(cur)]
    closure = is_op(cur, "+") and take(cur) is not None
    steps[0] = steps[0][:2] + (inverse, False)
    steps[-1] = steps[-1][:3] + (closure,)
    return steps


def _names(cur: list) -> list[tuple[str, str]]:
    """`a.b`, `rel:t`, `a.rel:t.b`... as `(field | rel, name)` pairs."""
    pairs = [("field", piece) for piece in expect_ident(cur).value.split(".")]
    if pairs[-1][1] == "rel" and is_op(cur, ":") and peek(cur, 1).kind == "ident":
        pairs.pop()
        take(cur)
        rest = _names(cur)
        pairs += [("rel", rest[0][1])] + rest[1:]
    return pairs


def reach(view: dict, item: dict, path: tuple) -> list[dict]:
    """The elements a path reaches from `item`; an unavailable one is an incomplete element."""
    frontier = [item]
    for step in path:
        frontier = _dedupe([el for origin in frontier for el in _from(view, origin, step)])
    return frontier


def _from(view: dict, origin: dict, step: tuple) -> list[dict]:
    if origin.get("incomplete"):
        return [origin]
    return reach_step(view, origin, step)


def _dedupe(items: list[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    for item in items:
        seen.setdefault(item["id"], item)
    return list(seen.values())
