"""`FieldCondition` → predicate tree, by the equivalence table (rules-language.md §7).

The value goes into the tree as a literal of any Python type (a bool, a list), so the
translation needs no literal syntax for it; the clause shows it written as the language would.
"""

from __future__ import annotations

import json
import re
from typing import Any

from sldb.store.graph.language.predicate_ast import Predicate
from sldb.store.query_engine.where_literal import quote, scalar_literal

_COMPARISON = {"eq": "=", "ne": "!=", "gt": ">", "lt": "<"}


def condition_predicate(field: str, op: str, value: Any) -> Predicate:
    """The parsed predicate equivalent to one `FieldCondition`."""
    root = _NULLS[op](field) if op in _NULLS else _VALUED.get(op, _comparison)(field, op, value)
    return Predicate(root[1], root)


def _has(field: str) -> tuple:
    return ("leaf", f"has({field})", "has", (field,))


def _contains(field: str, op: str, value: Any) -> tuple:
    return ("leaf", f"{written(value)} in {field}", "in", (("literal", value), ("field", field)))


def _starts_with(field: str, op: str, value: Any) -> tuple:
    pattern = "^" + re.escape(str(value))
    return ("leaf", f"{field} ~ {quote(pattern)}", "regex", (("field", field), re.compile(pattern)))


def _comparison(field: str, op: str, value: Any) -> tuple:
    symbol = _COMPARISON[op]
    return ("leaf", f"{field} {symbol} {written(value)}", "cmp", (("field", field), symbol, ("literal", value)))


_NULLS = {"is_not_null": _has, "is_null": lambda field: ("not", f"not has({field})", _has(field))}
_VALUED = {"contains": _contains, "starts_with": _starts_with}


def written(value: Any) -> str:
    """A value as the language writes it: a literal, a list of literals, else its JSON."""
    literal = scalar_literal(value)
    if literal is not None:
        return literal
    if isinstance(value, list) and all(scalar_literal(v) is not None for v in value):
        return "[" + ", ".join(scalar_literal(v) or "" for v in value) + "]"
    return json.dumps(value, default=str)
