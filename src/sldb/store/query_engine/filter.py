"""--where over one document: the predicate language (GO05), parsed once and matched per document."""

from __future__ import annotations

from typing import Any

from sldb.store.graph.language.predicate_documents import document_matcher


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
        return document_matcher(expression)(doc, resolve_model_ref, pythonpath)
