from __future__ import annotations
import re
from typing import Any
from sldb.cli.graph_ops import SearchRecord
from sldb.store.query_engine.filter import _where_matches as _core_where_matches
from sldb.cli.commands.find_utils import RuntimeDocProxy

class FindFilters:
    """Filters search records based on where expressions."""

    def __init__(self, pythonpath: str | None) -> None:
        self.pythonpath = pythonpath

    def matches(self, record: SearchRecord, expression: str) -> bool:
        """Check if a record matches a where expression."""
        if record.kind == "doc": return self._match_doc(record, expression)
        if record.kind == "field": return self._match_field(record, expression)
        if record.kind == "section": return self._match_section(record, expression)
        return True

    def _match_doc(self, record: SearchRecord, expression: str) -> bool:
        name = record.doc_name or record.name
        doc = RuntimeDocProxy(record.payload, name, record.model_type or self._model_proxy(record))
        return _core_where_matches(doc, expression, self._resolve_model_ref, self.pythonpath) # type: ignore[arg-type]

    def _match_field(self, record: SearchRecord, expression: str) -> bool:
        data = self._field_data(record)
        if expression.startswith("has("):
            key = expression[4:-1]
            return key in data and data[key] not in (None, "", [], {})
        return self._eval_field_op(data, expression)

    def _field_data(self, record: SearchRecord) -> dict[str, Any]:
        return {
            "value": record.value, "doc": record.doc_name, "model": record.model_name,
            "field": record.field_path, "path": record.path, "owning_section": record.owning_section or "",
        }

    def _eval_field_op(self, data: dict[str, Any], expression: str) -> bool:
        for op in ("=", "!="):
            if op in expression:
                left, right = [part.strip() for part in expression.split(op, 1)]
                expected = right[1:-1] if right.startswith('"') and right.endswith('"') else right
                actual = data.get(left)
                return (str(actual) == expected) if op == "=" else (str(actual) != expected)
        return False

    def _match_section(self, record: SearchRecord, expression: str) -> bool:
        if expression.startswith("title ~ "):
            pattern = expression.split("~", 1)[1].strip().strip('"')
            return re.search(pattern, record.title or "") is not None
        if expression.startswith("path = "):
            expected = expression.split("=", 1)[1].strip().strip('"')
            return record.path == expected
        return self._match_section_contains(record, expression)

    def _match_section_contains(self, record: SearchRecord, expression: str) -> bool:
        match = re.fullmatch(r'"([^"]+)"\s+in\s+(about|breadcrumbs|semantic_tags)', expression)
        if match:
            needle, field = match.groups()
            haystack = self._get_section_haystack(record, field)
            return needle in haystack
        return True

    def _get_section_haystack(self, record: SearchRecord, field: str) -> list[str]:
        if field == "about": return record.about or []
        if field == "breadcrumbs": return record.payload.get("breadcrumbs", [])
        if field == "semantic_tags": return list(record.semantic)
        return []

    def _model_proxy(self, record: SearchRecord) -> type:
        class _Proxy:
            __module__ = ""
        _Proxy.__name__ = record.model_name or "Model"
        return _Proxy

    @staticmethod
    def _resolve_model_ref(model_ref: str, pythonpath: str | None) -> Any:
        from sldb.cli.model_utils import resolve_model_ref
        return resolve_model_ref(model_ref, pythonpath)
