from __future__ import annotations

import re
from typing import Any

from sldb.store.query_engine.models import RuntimeDocument


def _where_matches(
    doc: RuntimeDocument, expression: str, resolve_model_ref, pythonpath: str | None
) -> bool:
    """Evaluates a --where filter expression against a document."""
    expression = expression.strip()
    # Simple has(field) check
    has_match = re.fullmatch(r"has\(([^)]+)\)", expression)
    if has_match:
        field = has_match.group(1)
        return field in doc.payload and doc.payload[field] not in (None, "")

    # "needle" in field check
    contains_match = re.fullmatch(r'"([^"]+)"\s+in\s+([A-Za-z_][\w]*)', expression)
    if contains_match:
        needle, field = contains_match.groups()
        value = doc.payload.get(field)
        return needle in value if isinstance(value, (list, str)) else False

    # field ~ "regex" check
    regex_match = re.fullmatch(r'([A-Za-z_][\w]*)\s*~\s*"([^"]+)"', expression)
    if regex_match:
        field, pattern = regex_match.groups()
        target = doc.name if field == "doc" else str(doc.payload.get(field, ""))
        return re.search(pattern, target) is not None

    # model inheritance check
    model_match = re.fullmatch(r"model\s*<=\s*([A-Za-z_][\w]*)", expression)
    if model_match:
        base_name = model_match.group(1)
        base_type = resolve_model_ref(f"{doc.model_type.__module__}:{base_name}", pythonpath)
        return issubclass(doc.model_type, base_type)

    # Comparison ops
    compare_match = re.fullmatch(
        r'([A-Za-z_][\w]*)\s*(=|!=|>=|<=)\s*("[^"]+"|\d+(?:\.\d+)?)', expression
    )
    if compare_match:
        field, op, raw_value = compare_match.groups()
        value = doc.payload.get(field)
        expected: Any = raw_value[1:-1] if raw_value.startswith('"') else float(raw_value)
        if op == "=":
            return value == expected
        if op == "!=":
            return value != expected
        if op == ">=":
            return value >= expected
        if op == "<=":
            return value <= expected
    return False
