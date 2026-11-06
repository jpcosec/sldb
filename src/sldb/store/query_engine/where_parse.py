"""Deprecated (GO05): the old `--where` grammar, now a shim over the predicate language.

`WherePredicateError` stays here: it is the error every parse of the language raises. The
grammar itself lives in `sldb.store.graph.language` (`parse_predicate`), a superset of the
old one with the same operators and results (rules-language.md §7). `compile_where` and
`where_parse` still work and emit `DeprecationWarning`; GO10 retires them.
"""

from __future__ import annotations

import warnings
from typing import Any, Callable

from sldb.store.exceptions import SLDBError

Predicate = Callable[[Any, Any, Any], bool]  # (doc, resolve_model_ref, pythonpath) -> bool
_USE = "use sldb.store.graph.language.parse_predicate / document_matcher (rules-language.md)"


class WherePredicateError(ValueError, SLDBError):
    """A predicate that does not parse."""

    def __init__(self, expression: str):
        super().__init__(f"no evaluator understands the predicate: {expression!r}")


def compile_where(expression: str) -> Predicate:
    """Deprecated: the document matcher of the predicate language for `expression`."""
    warnings.warn(f"compile_where is deprecated: {_USE}", DeprecationWarning, stacklevel=2)
    from sldb.store.graph.language.predicate_documents import document_matcher

    return document_matcher(expression)


def where_parse(expression: str) -> Any:
    """Deprecated: `parse_predicate(expression)` of the predicate language."""
    warnings.warn(f"where_parse is deprecated: {_USE}", DeprecationWarning, stacklevel=2)
    from sldb.store.graph.language.predicate_parser import parse_predicate

    return parse_predicate(expression)
