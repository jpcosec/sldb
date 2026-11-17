"""Statements of a Python module or class body as facts: `name = value` (or `name: T = value`) is an
`assignment`, a bare call (`router.register(...)`) is a `call` named by its func. Read at the top of
the module and in the body of each class that is a fact (a nested `Meta` too); a statement under `if`,
`try` or a function is not one, like definitions. An assignment's value: a call gives `attrs.call`
`{func, args, kwargs}`; a list or tuple gives `attrs.items`, one `{func, args, kwargs}` or `{value}`
per item, plus `attrs.value` when no item is a call; anything else gives `attrs.value`, its text.
An augmented assignment (`urlpatterns += [...]`, `x -= 1`, any operator) is an `assignment` too, with
`attrs.op` (`'+='`) and its value read as with `=`. A chained one (`a = b = value`) gives one fact per
name, each with the same value. Their ids come in the second pass of `Ids` (`take_late`), after every
module and definition. Not facts: a target that is not a plain name (`obj.attr = 1`, `p, q = f()`,
`x[0] = 1`; in a chain only those targets are skipped), an annotation without a value (`y: int`), an
expression statement that is not a call, and any statement under `if`, `for`, `with`, `try` or a def.
"""

from __future__ import annotations

import hashlib
from typing import Any

from sldb.code.facts import fact, key_of, rels
from sldb.code.ids import Ids
from sldb.code.py_calls import call_parts
from sldb.code.readers import field_text, first_statement, py_end_line, py_norm, text

_SEQUENCES = {"list", "tuple", "expression_list"}
_ASSIGNMENTS = {"assignment", "augmented_assignment"}


def statement_facts(owners: list[tuple[Any, str, str]], ctx: dict[str, Any], idgen: Ids) -> list[dict[str, Any]]:
    """Facts of the statements of each `(module or class node, owner id, owner qualified name)`."""
    out = []
    for node, oid, oq in owners:
        body = node if node.type == "module" else node.child_by_field_name("body")
        for stmt in body.named_children if body is not None else []:
            out.extend(_fact(*read, stmt, (oid, oq), ctx, idgen) for read in _reads(stmt, ctx["src"]))
    return out


def class_owners(items: list, names: dict, ids: dict) -> list[tuple[Any, str, str]]:
    """`(node, id, qualified name)` of each captured class that became a fact: the class-level owners."""
    return [(n, ids[key_of(n)], names[key_of(n)]) for cap, n in items if cap == "class" and key_of(n) in ids]


def _reads(stmt: Any, src: bytes) -> list[tuple[str, str, dict[str, Any]]]:
    """`(kind, name, attrs)` of each fact a statement gives: one call, one per assigned name, or none."""
    expr = first_statement(stmt) if stmt.type == "expression_statement" and stmt.named_child_count == 1 else None
    if expr is not None and expr.type == "call":
        parts = call_parts(expr, src)
        return [("call", parts["func"], {"call": parts})]
    if expr is None or expr.type not in _ASSIGNMENTS or expr.child_by_field_name("right") is None:
        return []
    targets, value = _chain(expr)
    op = {"op": field_text(expr, src, "operator")} if expr.type == "augmented_assignment" else {}
    attrs = {**op, **value_attrs(value, src)}
    return [("assignment", text(t, src), attrs) for t in targets if t.type == "identifier"]


def _chain(expr: Any) -> tuple[list[Any], Any]:
    """The targets of `a = b = value` from left to right, and the value."""
    targets = []
    while expr.type in _ASSIGNMENTS and expr.child_by_field_name("right") is not None:
        targets.append(expr.child_by_field_name("left"))
        expr = expr.child_by_field_name("right")
    return targets, expr


def value_attrs(value: Any, src: bytes) -> dict[str, Any]:
    if value.type == "call":
        return {"call": call_parts(value, src)}
    if value.type not in _SEQUENCES:
        return {"value": py_norm(text(value, src))}
    items = [call_parts(i, src) if i.type == "call" else {"value": py_norm(text(i, src))} for i in value.named_children if i.type != "comment"]
    return {"items": items} if any("func" in i for i in items) else {"items": items, "value": py_norm(text(value, src))}


def _fact(kind: str, name: str, attrs: dict, stmt: Any, owner: tuple[str, str], ctx: dict[str, Any], idgen: Ids) -> dict[str, Any]:
    q, module, normalized = f"{owner[1]}.{name}" if owner[1] else name, ctx["module"], py_norm(text(stmt, ctx["src"]))
    return idgen.take_late(f"{module}.{q}" if module else q, fact(kind=kind, name=name, qualified_name=q, path=ctx["rel"],
                span={"start_line": stmt.start_point[0] + 1, "end_line": py_end_line(stmt)}, source_hash=ctx["digest"], relations=rels(owner[0]),
                attrs={"native_kind": first_statement(stmt).type, "module": module, **attrs},
                fingerprints={"signature": _sha(normalized), "shape": _sha(normalized.replace(name, "_", 1)), "docstring": None, "body": _sha(normalized)}))


def _sha(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()
