"""The error every parse of the predicate language raises (rules-language.md).

A `ValueError` as well as an `SLDBError`: a predicate that does not parse is a bad value.
"""

from __future__ import annotations

from .sldb_error import SLDBError


class WherePredicateError(ValueError, SLDBError):
    """A predicate that does not parse."""

    def __init__(self, expression: str):
        super().__init__(f"no evaluator understands the predicate: {expression!r}")
