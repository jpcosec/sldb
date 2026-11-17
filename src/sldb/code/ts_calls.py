"""Calls in TypeScript/JavaScript source as text, with no type or import resolved, in the form of
Python's (`py_calls`): the calls a function, hook or component makes (`fetch`, `axios.get`,
`api.posts.create`), one `{name, line, first_arg}` per call in source order. `name` is the whole
called expression, unsplit, in the canonical form of `ts_callee` (built from the tree: no whitespace,
no `await`, no type arguments, `()` for a call in the chain, `(fn)`, `[]`) and `canonical: true`, or,
for a chain that starts at an array, a binary, a `new`, a literal or the like, its collapsed text
(`ts_loose`) and `canonical: false`; `first_arg` is a first
argument that is a string or a template without `${...}`, without its quotes or backticks (escapes
as written), else None. Like a
nested `def` in Python, a nested `function`, generator or `class` declaration is not walked; an
arrow function or function expression is (a callback, an inline handler), like a `lambda`. `new X()`
is not a call.
"""

from __future__ import annotations

from typing import Any

from sldb.code.readers import first_statement, text
from sldb.code.ts_callee import call_name

_NESTED = {"function_declaration", "generator_function_declaration", "class_declaration", "class"}
_LITERALS = {"string", "template_string"}


def body_nodes(fn: Any) -> list[Any]:
    """The nodes of a function's body in source order (pre-order), without entering a nested declaration."""
    out, stack = [], [fn.child_by_field_name("body")]
    while stack:
        n = stack.pop()
        if n is None or n.type in _NESTED:
            continue
        out.append(n)
        stack.extend(reversed(n.named_children))
    return out


def callee(call: Any, src: bytes) -> tuple[str, bool]:
    """`(name, canonical)` of the `function` field (`ts_callee`); the grammar reads `await f<T>(...)` as
    a call whose function is `await f`, and `call_name` sees through that `await`."""
    return call_name(call.child_by_field_name("function"), src)


def first_arg(call: Any, src: bytes) -> str | None:
    args = call.child_by_field_name("arguments")
    lit = first_statement(args) if args is not None and args.type == "arguments" else args
    if lit is None or lit.type not in _LITERALS or any(c.type == "template_substitution" for c in lit.named_children):
        return None
    return text(lit, src)[1:-1]


def body_calls(nodes: list[Any], src: bytes) -> list[dict[str, Any]]:
    """`{name, line, first_arg, canonical}` of each call among `nodes`, in source order."""
    return [_call(n, src) for n in nodes if n.type == "call_expression"]


def _call(node: Any, src: bytes) -> dict[str, Any]:
    name, canonical = callee(node, src)
    return {"name": name, "line": node.start_point[0] + 1, "first_arg": first_arg(node, src), "canonical": canonical}
