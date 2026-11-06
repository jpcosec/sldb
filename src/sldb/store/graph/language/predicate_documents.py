"""The predicate language over a tracked document or a lone payload (the `--where` path).

A document's node reads its payload, its name, and its model family from the class's MRO by
name (`model <= X` as `--where` always read it). With no graph every path reaches nothing;
`find --where` passes the store's view so paths follow the index (`sldb.api.where`).
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.graph.language.predicate_api import as_predicate, node_finding
from sldb.store.graph.language.predicate_view import make_view, node, with_node

EMPTY_VIEW = make_view({}, [])


def document_node(doc: Any, node_id: str | None = None) -> dict[str, Any]:
    """The view node of a runtime document (`payload`, `name`, `model_type`)."""
    names = [c.__name__ for c in getattr(getattr(doc, "model_type", None), "__mro__", ())]
    model_name = getattr(doc, "model_name", None) or (names[0] if names else "")
    return node(node_id or f"{model_name}:{doc.name}", names[0] if names else None, doc.payload, names[1:], doc.name)


def document_finding(predicate: Any, item: dict[str, Any], view: dict[str, Any] = EMPTY_VIEW) -> dict[str, Any]:
    """The finding of one document node; paths read `view` (default: no graph)."""
    return node_finding(predicate, with_node(view, item), item)


def document_matcher(expression: Any) -> Callable[..., bool]:
    """`(doc, resolve_model_ref=None, pythonpath=None) -> bool`, parsed once (raises
    WherePredicateError when the expression does not parse)."""
    parsed = as_predicate(expression)
    return lambda doc, *_: document_finding(parsed, document_node(doc))["holds"] == "true"


def payload_holds(expression: Any, payload: dict, subject: dict | None = None, name: str = "") -> bool:
    """Whether a predicate holds on a lone payload; `{field}` reads `subject` (default: the
    payload). An empty expression always holds; `model <=` never does (no model)."""
    if isinstance(expression, str) and not expression.strip():
        return True
    item = node(name, None, payload, (), name)
    return node_finding(expression, EMPTY_VIEW, item, subject)["holds"] == "true"


def has_paths(expression: Any) -> bool:
    """Whether a predicate walks the graph (a quantifier or a `count`)."""
    from sldb.store.graph.language.predicate_ast import walk

    return any(n[0] in ("quant", "count") for n in walk(as_predicate(expression).root))
