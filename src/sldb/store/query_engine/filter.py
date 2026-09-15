"""--where over one document: sldb's predicate grammar, parsed once and matched per document."""

from __future__ import annotations

from typing import Any

from sldb.store.query_engine.where_parse import compile_where


def _where_matches(
    doc: Any, expression: str, resolve_model_ref: Any, pythonpath: Any
) -> bool:
    """Evaluates a --where filter expression against a document."""
    return DocumentFilter.where_matches(doc, expression, resolve_model_ref, pythonpath)


class DocumentFilter:
    """Filter engine for matching documents against query expressions."""

    @classmethod
    def where_matches(
        cls, doc: Any, expression: str, resolve_model_ref: Any, pythonpath: Any
    ) -> bool:
        """Matches one document; a predicate no evaluator parses raises WherePredicateError."""
        return compile_where(expression)(doc, resolve_model_ref, pythonpath)
