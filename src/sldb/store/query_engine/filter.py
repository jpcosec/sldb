from __future__ import annotations

import re
from typing import Any

from sldb.store.query_engine.models import RuntimeDocument


def _where_matches(
    doc: RuntimeDocument, expression: str, resolve_model_ref, pythonpath: str | None
) -> bool:
    """Evaluates a --where filter expression against a document."""
    return DocumentFilter.where_matches(doc, expression, resolve_model_ref, pythonpath)

class DocumentFilter:
    """Filter engine for matching documents against query expressions."""

    @classmethod
    def where_matches(
        cls, doc: RuntimeDocument, expression: str, resolve_model_ref, pythonpath: str | None
    ) -> bool:
        """Evaluates a --where filter expression against a document."""
        expression = expression.strip()
        if cls._eval_has(doc, expression): return True
        if cls._eval_contains(doc, expression): return True
        if cls._eval_regex(doc, expression): return True
        if cls._eval_model(doc, expression, resolve_model_ref, pythonpath): return True
        if cls._eval_compare(doc, expression): return True
        return False

    @classmethod
    def _eval_has(cls, doc: RuntimeDocument, expression: str) -> bool:
        has_match = re.fullmatch(r"has\(([^)]+)\)", expression)
        if not has_match:
            return False
        field = has_match.group(1)
        return field in doc.payload and doc.payload[field] not in (None, "")

    @classmethod
    def _eval_contains(cls, doc: RuntimeDocument, expression: str) -> bool:
        contains_match = re.fullmatch(r'"([^"]+)"\s+in\s+([A-Za-z_][\w]*)', expression)
        if not contains_match:
            return False
        needle, field = contains_match.groups()
        value = doc.payload.get(field)
        return needle in value if isinstance(value, (list, str)) else False

    @classmethod
    def _eval_regex(cls, doc: RuntimeDocument, expression: str) -> bool:
        regex_match = re.fullmatch(r'([A-Za-z_][\w]*)\s*~\s*"([^"]+)"', expression)
        if not regex_match:
            return False
        field, pattern = regex_match.groups()
        target = doc.name if field == "doc" else str(doc.payload.get(field, ""))
        return re.search(pattern, target) is not None

    @classmethod
    def _eval_model(cls, doc: RuntimeDocument, expression: str, resolve_model_ref, pythonpath: str | None) -> bool:
        model_match = re.fullmatch(r"model\s*<=\s*([A-Za-z_][\w]*)", expression)
        if not model_match:
            return False
        from sldb.store.query_engine.structural import model_in_family
        return model_in_family(doc.model_type, model_match.group(1))

    @classmethod
    def _eval_compare(cls, doc: RuntimeDocument, expression: str) -> bool:
        compare_match = re.fullmatch(
            r'([A-Za-z_][\w]*)\s*(=|!=|>=|<=)\s*("[^"]+"|\d+(?:\.\d+)?)', expression
        )
        if not compare_match:
            return False
        field, op, raw_value = compare_match.groups()
        value = doc.payload.get(field)
        expected: Any = raw_value[1:-1] if raw_value.startswith('"') else float(raw_value)
        return cls._apply_op(value, op, expected)

    @classmethod
    def _apply_op(cls, value: Any, op: str, expected: Any) -> bool:
        if op == "=": return value == expected
        if op == "!=": return value != expected
        if op == ">=": return value >= expected
        if op == "<=": return value <= expected
        return False
