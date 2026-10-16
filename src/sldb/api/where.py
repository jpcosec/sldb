"""`--where` as a library: test one predicate against a plain payload, tracked or not."""

from __future__ import annotations

from typing import Any

from sldb.store.query_engine.where_subject import payload_matches


def where_matches(expression: str, payload: dict[str, Any], subject: dict[str, Any] | None = None) -> bool:
    """Whether a `--where` predicate holds on `payload` (the grammar of `sldb find --where`).

    Args:
        expression: Predicates joined by ` and `: `has(f)`, `nonempty(f)`, `"x" in f`,
            `f ~ "re"`, `f = "s"`, `f >= 3`, ...; empty always holds.
        payload: The fields the predicate reads; need not belong to a tracked document.
        subject: Fills `{field}` placeholders (default: `payload`). A placeholder the subject
            lacks, or holds as a list or dict, makes the expression not hold.

    Raises:
        WherePredicateError: No evaluator parses some part of the expression.
    """
    return payload_matches(expression, payload, subject)
