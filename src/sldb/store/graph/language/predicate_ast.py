"""The parsed predicate: its source text and its tree (rules-language.md §1-§2).

The tree is plain tuples, tag first, each node carrying its clause (the source text it was
parsed from) so an explanation can name what decided a result:

    ("and" | "or", clause, left, right)      ("not", clause, child)
    ("leaf", clause, kind, args)             kind: has, nonempty, model, in, regex, cmp
    ("quant", clause, any|all|none, path, body)
    ("count", clause, path, body, op, term)

A term is `("field", name)`, `("literal", value)` or `("subst", name)` (`{name}`, read from
the subject). A path is a tuple of steps `(field|rel, name, inverse, closure)`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Predicate:
    """A predicate of the language, parsed once and evaluated many times."""

    text: str
    root: tuple

    def __str__(self) -> str:
        return self.text


def walk(node: tuple):
    """Every node of a tree, the root first."""
    yield node
    for child in children(node):
        yield from walk(child)


def children(node: tuple) -> list[tuple]:
    """The sub-predicates of a node (a quantifier's body, a boolean's operands)."""
    if node[0] in ("and", "or"):
        return [node[2], node[3]]
    if node[0] == "not":
        return [node[2]]
    if node[0] == "quant":
        return [node[4]]
    return [node[3]] if node[0] == "count" else []


def substitutions(root: tuple) -> list[str]:
    """The `{field}` names a tree reads from its subject, in order, without repeats."""
    names = [term[1] for node in walk(root) for term in _terms(node) if term[0] == "subst"]
    return list(dict.fromkeys(names))


def top_level_models(root: tuple) -> list[str]:
    """The `model <= X` bases of the top-level conjunction (they restrict the domain, §6)."""
    if root[0] == "and":
        return top_level_models(root[2]) + top_level_models(root[3])
    return [root[3][0]] if root[0] == "leaf" and root[2] == "model" else []


def _terms(node: tuple) -> list[tuple]:
    if node[0] == "count":
        return [node[5]]
    if node[0] == "leaf" and node[2] in ("in", "cmp"):
        return [node[3][0], node[3][-1]]
    return [node[3][0]] if node[0] == "leaf" and node[2] == "regex" else []
