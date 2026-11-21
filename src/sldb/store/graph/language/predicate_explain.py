"""Boolean logic over `(value, clause, seen)` results, and the finding they become (§3, §4).

`value` is True or False. `seen` follows rules-language.md §4: an `and` keeps the first false
branch, an `or` the first true one, a quantifier its witness (the first element that falsifies
an `all` or satisfies an `any`).
"""

from __future__ import annotations

from typing import Any

from sldb.store.graph.language.predicate_leaves import compare, resolve

_HOLDS = {True: "true", False: "false"}


def finding(node: str, value: bool, clause: str, seen: dict[str, Any]) -> dict[str, Any]:
    """One finding: `node`, `holds` (`true`/`false`), `clause`, `seen`."""
    return {"node": node, "holds": _HOLDS[value], "clause": clause, "seen": seen}


def junction(word: str, clause: str, left: tuple, right_of) -> tuple:
    """`and` (`word` decides on False) or `or` (on True), right evaluated only when needed."""
    decisive = word == "or"
    if left[0] is decisive:
        return left
    right = right_of()
    if right[0] is decisive:
        return right
    return not decisive, clause, {**left[2], **right[2]}


def quantified(kind: str, clause: str, results: list[tuple]) -> tuple:
    """`any`, `all` or `none` over the elements' results."""
    if kind == "none":
        value, _, seen = quantified("any", clause, results)
        return not value, clause, seen
    decisive = kind == "any"
    witness = _first(results, decisive)
    return (witness[0], clause, witness[2]) if witness else (not decisive, clause, {})


def counted(node: tuple, item: dict, ctx: dict, results: list[tuple]) -> tuple:
    """`count(path: p) cmp term` over the elements that hold `p`."""
    right, seen = resolve(node[5], item, ctx)
    return compare(sum(1 for r in results if r[0] is True), node[4], right), node[1], seen


def _first(results: list[tuple], value: bool) -> tuple | None:
    return next((r for r in results if r[0] is value), None)
