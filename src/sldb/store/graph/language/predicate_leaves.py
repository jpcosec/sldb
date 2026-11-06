"""The leaves of the language over one element: `(holds, seen)` for each atom kind.

A field is read by its exact key, else by dotted path (`where_lookup`, H9). An absent field
holds no comparison, membership or regex; `doc ~ "re"` reads the document's name, as the
`~` of `--where` always did. A comparison Python cannot make (`"a" < 1`) is false.
"""

from __future__ import annotations

import operator
from typing import Any

from sldb.store.query_engine.where_lookup import _ABSENT, _lookup

_COMPARE = {"=": operator.eq, "!=": operator.ne, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge}
_SIZED = (str, list, dict, tuple, set)


def leaf_value(kind: str, args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    """Whether one atom holds on `item`, and the fields it read."""
    return _LEAVES[kind](args, item, ctx)


def lookup(payload: dict, field: str) -> Any:
    """A field by exact key, else by dotted path; `_ABSENT` when there is none."""
    return payload[field] if field in payload else _lookup(payload, field, _ABSENT)


def compare(left: Any, op: str, right: Any) -> bool:
    """One comparison; false when either side is absent or Python cannot compare them."""
    try:
        return left is not _ABSENT and right is not _ABSENT and bool(_COMPARE[op](left, right))
    except TypeError:
        return False


def resolve(term: tuple, item: dict, ctx: dict) -> tuple[Any, dict[str, Any]]:
    """A term's value and the `seen` entry it adds."""
    if term[0] == "literal":
        return term[1], {}
    if term[0] == "subst":
        return ctx["subst"][term[1]], {}
    value = lookup(item["payload"], term[1])
    return value, {term[1]: None if value is _ABSENT else value}


def _has(args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    value, seen = resolve(("field", args[0]), item, ctx)
    return value is not _ABSENT and value is not None and value != "", seen


def _nonempty(args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    value, seen = resolve(("field", args[0]), item, ctx)
    empty = isinstance(value, _SIZED) and len(value) == 0
    return value is not _ABSENT and value is not None and not empty, seen


def _model(args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    model = item.get("model")
    return model is not None and (model == args[0] or args[0] in item.get("base_models", ())), {"model": model}


def _in(args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    (left, left_seen), (right, right_seen) = resolve(args[0], item, ctx), resolve(args[1], item, ctx)
    try:
        holds = left is not _ABSENT and isinstance(right, (list, str)) and left in right
    except TypeError:
        holds = False
    return bool(holds), {**left_seen, **right_seen}


def _regex(args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    if args[0] == ("field", "doc"):
        return args[1].search(item.get("name") or "") is not None, {"doc": item.get("name")}
    value, seen = resolve(args[0], item, ctx)
    return value is not _ABSENT and value is not None and args[1].search(str(value)) is not None, seen


def _cmp(args: tuple, item: dict, ctx: dict) -> tuple[bool, dict[str, Any]]:
    (left, left_seen), (right, right_seen) = resolve(args[0], item, ctx), resolve(args[2], item, ctx)
    return compare(left, args[1], right), {**left_seen, **right_seen}


_LEAVES = {"has": _has, "nonempty": _nonempty, "model": _model, "in": _in, "regex": _regex, "cmp": _cmp}
