import re
from typing import Any

from sldb.cli.commands.find_proxy import _RuntimeDocProxy
from sldb.cli.graph_ops import SearchRecord
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query_engine.filter import _where_matches as core_where_matches

def _model_proxy(record: SearchRecord) -> type:
    class _Proxy:
        __module__ = ""

    _Proxy.__name__ = record.model_name or "Model"
    return _Proxy

def _where_matches_doc(record: SearchRecord, expression: str, pythonpath: str | None) -> bool:
    runtime_doc = _RuntimeDocProxy(  # `sldb.<key>`: the provenance block is addressable like a field
        payload={**record.payload, "sldb": record.provenance or {}}, name=record.doc_name or record.name, model_type=_model_proxy(record)
    )
    return core_where_matches(runtime_doc, expression, resolve_model_ref, pythonpath) # type: ignore[arg-type]

def _where_matches_field(record: SearchRecord, expression: str) -> bool:
    data = {"value": record.value, "doc": record.doc_name, "model": record.model_name, "field": record.field_path, "path": record.path, "owning_section": record.owning_section or ""}
    if expression.startswith("has("): return _where_matches_field_has(data, expression)
    for op in ("=", "!="):
        if op in expression: return _where_matches_field_op(data, expression, op)
    return False

def _where_matches_field_has(data: dict, expression: str) -> bool:
    key = expression[4:-1]
    return key in data and data[key] not in (None, "", [], {})

def _where_matches_field_op(data: dict, expression: str, op: str) -> bool:
    left, right = [part.strip() for part in expression.split(op, 1)]
    expected = right[1:-1] if right.startswith('"') and right.endswith('"') else right
    actual = data.get(left)
    return (str(actual) == expected) if op == "=" else (str(actual) != expected)

def _where_matches_section(record: SearchRecord, expression: str) -> bool:
    if expression.startswith("title ~ "):
        return re.search(expression.split("~", 1)[1].strip().strip('"'), record.title or "") is not None
    contains_match = re.fullmatch(r'"([^"]+)"\s+in\s+(about|breadcrumbs|semantic_tags)', expression)
    if contains_match: return _where_matches_section_contains(record, contains_match)
    if expression.startswith("path = "): return record.path == expression.split("=", 1)[1].strip().strip('"')
    return True

def _where_matches_section_contains(record: SearchRecord, contains_match: Any) -> bool:
    needle, field = contains_match.groups()
    if field == "about": return needle in (record.about or [])
    if field == "breadcrumbs": return needle in record.payload.get("breadcrumbs", [])
    if field == "semantic_tags": return needle in record.semantic
    return False

def where_matches(record: SearchRecord, expression: str, pythonpath: str | None) -> bool:
    if record.kind == "doc": return _where_matches_doc(record, expression, pythonpath)
    if record.kind == "field": return _where_matches_field(record, expression)
    if record.kind == "section": return _where_matches_section(record, expression)
    return True
