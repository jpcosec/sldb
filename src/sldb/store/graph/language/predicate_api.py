"""The one predicate API (GO05): what `--where`, `where_matches`, `edges_holding`,
`StructuredQuery` and `GraphBackend.eval` all evaluate through.

`findings` is `eval(predicate, subject=None)` of rules-language.md §6 over a graph view: with
a subject, its one finding; without, one per document of the domain (every document, or the
families a top-level `model <=` conjunction names, intersected).
"""

from __future__ import annotations

from typing import Any

from sldb.store.graph.language.predicate_ast import Predicate, substitutions, top_level_models
from sldb.store.graph.language.predicate_eval import evaluate
from sldb.store.graph.language.predicate_explain import finding
from sldb.store.graph.language.predicate_parser import parse_predicate
from sldb.store.query_engine.where_literal import scalar_literal


def as_predicate(predicate: Any) -> Predicate:
    """A parsed predicate, parsing text (WherePredicateError when it does not parse)."""
    return predicate if isinstance(predicate, Predicate) else parse_predicate(str(predicate))


def node_finding(predicate: Any, view: dict, item: dict, subject: dict | None = None) -> dict[str, Any]:
    """The finding of `item`; `{field}` reads `subject` (default: the item's own payload)."""
    parsed, source = as_predicate(predicate), item["payload"] if subject is None else subject
    values = _substituted(parsed, source)
    if None in values.values():
        return finding(item["id"], False, parsed.text, {n: source.get(n) for n in values})
    return finding(item["id"], *evaluate(parsed.root, item, {"view": view, "subst": values}))


def findings(predicate: Any, view: dict, subject: str | None = None) -> list[dict[str, Any]]:
    """`eval(predicate, subject)` over a view: one finding for the subject, else the domain's."""
    parsed = as_predicate(predicate)
    if subject is not None:
        item = view["node"](subject)
        if item is None:
            raise ValueError(f"sin nodo {subject}")
        return [node_finding(parsed, view, item)]
    return [node_finding(parsed, view, item) for item in domain(parsed, view)]


def domain(predicate: Predicate, view: dict) -> list[dict]:
    """The documents a subject-less evaluation covers (§6)."""
    bases = top_level_models(predicate.root)
    items = [view["node"](i) for i in view["ids"]()]
    return [i for i in items if i is not None and all(b == i["model"] or b in i["base_models"] for b in bases)]


def _substituted(parsed: Predicate, subject: dict) -> dict[str, Any]:
    """`{field}` values; a missing or non-scalar one maps to None (the predicate then fails)."""
    names = substitutions(parsed.root)
    return {n: subject.get(n) if scalar_literal(subject.get(n)) is not None else None for n in names}
