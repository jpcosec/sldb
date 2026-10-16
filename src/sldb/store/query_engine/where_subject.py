"""A `--where` predicate on a plain payload, with `{field}` filled from a subject.

An edge's condition names fields of the document it is tested on, and may name fields of a
subject in braces (`capacity >= {party_size}`). Braces are filled only outside literals,
each with the subject's value written as a literal; a brace whose field the subject lacks,
or holds a non-scalar, makes the condition not hold, as an absent field does.
"""

from __future__ import annotations

import re
from types import SimpleNamespace
from typing import Any

from sldb.store.query_engine.where_literal import LITERAL, scalar_literal
from sldb.store.query_engine.where_parse import compile_where

_BRACE = re.compile(f"({LITERAL})|\\{{([A-Za-z_]\\w*)\\}}")


def fill_braces(expression: str, subject: dict[str, Any]) -> tuple[str, bool]:
    """`expression` with every `{field}` replaced by the subject's value, and whether all were.

    A brace that cannot be filled becomes a placeholder literal, so the expression still parses.
    """
    missing: list[str] = []

    def fill(m: re.Match) -> str:
        if m.group(1) is not None:
            return m.group(1)
        written = scalar_literal(subject.get(m.group(2)))
        missing.extend([] if written is not None else [m.group(2)])
        return written if written is not None else '"?"'

    return _BRACE.sub(fill, expression), not missing


def payload_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None = None, name: str = "") -> bool:
    """Whether `expression` holds on `payload`; `{field}` reads `subject` (default: `payload`).

    `doc ~ "..."` reads `name`; `model <= X` never holds, a payload carries no model class.
    An empty expression always holds. Raises WherePredicateError when it does not parse.
    """
    if not expression.strip():
        return True
    filled, complete = fill_braces(expression, payload if subject is None else subject)
    predicate = compile_where(filled)
    return complete and predicate(SimpleNamespace(payload=payload, name=name, model_type=None), None, None)
