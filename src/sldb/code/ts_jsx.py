"""The JSX attributes of a component that bind an event to a handler, without knowing any framework:
an attribute whose name is `on` followed by an uppercase letter (`onClick`, not `only`) and whose
value is `{identifier}` (`onClick={handleSave}` gives `handleSave`), `{call(...)}` or a function whose
body is a call (`{() => save(x)}`, `{() => { save(x); }}`), which give the called expression (`save`). Anything else (a member
expression, a string, a spread) is not a handler. `element` is the tag's name as written
(`button`, `Button`, `Form.Item`). A call's handler is named as `ts_callee` names it; a
non-canonical one is listed but gets no `calls` relation (`lang_ts`).
"""

from __future__ import annotations

from typing import Any

from sldb.code.readers import field_text, first_statement, text
from sldb.code.ts_calls import callee

_FUNCTIONS = {"arrow_function", "function_expression", "function"}


def jsx_handlers(nodes: list[Any], src: bytes) -> list[dict[str, str]]:
    """`{element, attribute, handler}` of each handler attribute among `nodes`, in source order."""
    out = []
    for n in nodes:
        name = text(n.named_children[0], src) if n.type == "jsx_attribute" else ""
        handler = _handler(n.named_children[-1], src) if _is_event(name) and n.named_child_count == 2 else None
        if handler is not None:
            out.append({"element": field_text(n.parent, src, "name"), "attribute": name, "handler": handler})
    return out


def _is_event(name: str) -> bool:
    return name.startswith("on") and name[2:3].isupper()


def _handler(value: Any, src: bytes) -> str | None:
    expr = first_statement(value) if value.type == "jsx_expression" else None
    if expr is not None and expr.type in _FUNCTIONS:
        expr = _inner_call(expr.child_by_field_name("body"))
    if expr is None or expr.type not in ("identifier", "call_expression"):
        return None
    return text(expr, src) if expr.type == "identifier" else callee(expr, src)[0]


def _inner_call(body: Any) -> Any:
    """A function body's call: the body itself, or a block whose first statement is a call."""
    stmt = first_statement(body) if body is not None and body.type == "statement_block" else body
    inner = first_statement(stmt) if stmt is not None and stmt.type == "expression_statement" else stmt
    return inner if inner is not None and inner.type == "call_expression" else None
