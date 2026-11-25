"""What `model_tag("Q")` reaches: the tag semantic DAG, read through the edges it already has.

A document's model declares tags (`__semantics__`). The predicate holds when one of them is
`Q`, descends from `Q` (`semantic_parent` edges, child -> parent, at any depth) or is
equivalent to either (`semantic_equivalent`, read in both directions: the DAG keeps one edge
per declaration but an equivalence is symmetric). Asking the parent reaches the children,
never the other way round. No second hierarchy is computed: `scope` only walks those edges.
"""

from __future__ import annotations

from typing import Any, Callable


def scope(tag: str, children: Callable[[str], list[str]], equivalents: Callable[[str], list[str]]) -> set[str]:
    """`tag`, what descends from it and what is equivalent to any of those."""
    found: set[str] = set()
    pending = [tag]
    while pending:
        current = pending.pop()
        if current not in found:
            found.add(current)
            pending += [*children(current), *equivalents(current)]
    return found


def invert(table: dict[str, list[str]]) -> dict[str, list[str]]:
    """`{a: [b]}` as `{b: [a]}`."""
    inverted: dict[str, list[str]] = {}
    for key, values in table.items():
        for value in values:
            inverted.setdefault(value, []).append(key)
    return inverted


def symmetric(table: dict[str, list[str]]) -> dict[str, list[str]]:
    """Each pair of `{a: [b]}` read in both directions."""
    both = invert(table)
    for key, values in table.items():
        both[key] = [*both.get(key, []), *values]
    return both


def dict_semantics(semantic: dict[str, Any]) -> dict[str, Callable]:
    """The view entries of `{model_tags: {model: [tag]}, parents: {tag: [parent]}, equivalents:
    {tag: [tag]}}` (the form of the test graphs of rules-language.md §8)."""
    parents, kids = semantic.get("parents") or {}, invert(semantic.get("parents") or {})
    equal, model_tags = symmetric(semantic.get("equivalents") or {}), semantic.get("model_tags") or {}
    known = {*parents, *kids, *equal, *(t for tags in model_tags.values() for t in tags)}
    return {
        "model_tags": lambda model: set(model_tags.get(model, ())),
        "tag_scope": lambda tag: scope(tag, lambda t: kids.get(t, []), lambda t: equal.get(t, [])),
        "tag_known": lambda tag: tag in known,
    }
