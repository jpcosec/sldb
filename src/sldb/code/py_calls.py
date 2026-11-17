"""Calls in Python source as text, with no type or import resolved: a call's `{func, args, kwargs}`,
a definition's decorators and bases, and the calls a function's body makes (`self.publish`,
`Post.objects.create`, `can_publish`). Every text goes through `py_norm`, like `signature`.
"""

from __future__ import annotations

from typing import Any

from sldb.code.readers import field_text, first_statement, py_norm, text

_NESTED = {"function_definition", "class_definition"}


def call_parts(call: Any, src: bytes) -> dict[str, Any]:
    """`{func, args, kwargs}` of a `call` node; `*x`, `**x` and a generator argument go to `args` as text."""
    arguments = call.child_by_field_name("arguments")
    items = [a for a in arguments.named_children if a.type != "comment"] if arguments.type == "argument_list" else [arguments]
    kwargs = {field_text(a, src, "name"): py_norm(field_text(a, src, "value")) for a in items if a.type == "keyword_argument"}
    args = [py_norm(text(a, src)) for a in items if a.type != "keyword_argument"]
    return {"func": py_norm(text(call.child_by_field_name("function"), src)), "args": args, "kwargs": kwargs}


def decorators(node: Any, src: bytes) -> list[dict[str, Any]]:
    """`{name, args, kwargs}` of each decorator of a definition, in order; a bare `@x` has no arguments."""
    parent = node.parent
    if parent is None or parent.type != "decorated_definition":
        return []
    exprs = [first_statement(d) for d in parent.children if d.type == "decorator"]
    return [_decorator(e, src) for e in exprs if e is not None]


def _decorator(expr: Any, src: bytes) -> dict[str, Any]:
    if expr.type != "call":
        return {"name": py_norm(text(expr, src)), "args": [], "kwargs": {}}
    parts = call_parts(expr, src)
    return {"name": parts["func"], "args": parts["args"], "kwargs": parts["kwargs"]}


def bases(node: Any, src: bytes) -> list[str]:
    """The bases a class writes, in order (`metaclass=` and other keywords are not bases)."""
    supers = node.child_by_field_name("superclasses")
    named = supers.named_children if supers is not None else []
    return [py_norm(text(b, src)) for b in named if b.type not in ("keyword_argument", "comment")]


def body_calls(node: Any, src: bytes) -> list[dict[str, Any]]:
    """`{name, line}` of each call in a function's body in source order; a nested def or class is not walked."""
    out, stack = [], list(reversed(node.child_by_field_name("body").named_children))
    while stack:
        n = stack.pop()
        if n.type in _NESTED:
            continue
        if n.type == "call":
            out.append({"name": py_norm(text(n.child_by_field_name("function"), src)), "line": n.start_point[0] + 1})
        stack.extend(reversed(n.named_children))
    return out


def definition_extras(node: Any, src: bytes) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """The relations and attrs a definition adds: `extends` and `bases` for a class, `calls` for a function."""
    attrs: dict[str, Any] = {"decorators": decorators(node, src)}
    if node.type == "class_definition":
        written = bases(node, src)
        return [{"type": "extends", "target": b} for b in dict.fromkeys(written)], {**attrs, "bases": written}
    calls = body_calls(node, src)
    return [{"type": "calls", "target": t} for t in sorted({c["name"] for c in calls})], {**attrs, "calls": calls}
