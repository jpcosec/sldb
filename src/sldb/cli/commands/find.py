from __future__ import annotations

import json
import re
from typing import Any

import yaml

from sldb.cli.graph import SearchRecord, iter_search_records, search_records
from sldb.store.query_engine.filter import _where_matches


class _RuntimeDocProxy:
    payload: dict[str, Any]
    name: str
    model_type: type

    def __init__(self, payload: dict[str, Any], name: str, model_type: type) -> None:
        self.payload = payload
        self.name = name
        self.model_type = model_type


class FindCLI:
    """Unified semantic + physical retrieval."""

    def run(self, args: Any) -> int:
        records = iter_search_records(
            args.store,
            args.pythonpath,
            include_linked=args.global_scope,
            rebuild=getattr(args, "rebuild", False),
        )
        kinds = {args.type} if args.type != "all" else None
        matched = search_records(
            records,
            args.term,
            search_in=args.search_in,
            regex=args.regex,
            fuzzy=args.fuzzy,
            kinds=kinds,
        )

        if args.where:
            matched = [
                record
                for record in matched
                if self._where_matches(record, args.where, args.pythonpath)
            ]

        payload = [self._serialize(record) for record in matched]
        if args.select:
            fields = [part.strip() for part in args.select.split(",") if part.strip()]
            payload = [{key: item.get(key) for key in fields} for item in payload]

        if args.format == "text":
            for item in payload:
                print(self._format_line(item))
        elif args.format == "yaml":
            print(
                yaml.safe_dump(
                    {"results": payload}, sort_keys=False, allow_unicode=True
                )
            )
        else:
            print(json.dumps({"results": payload}, indent=2))
        return 0 if payload else 1

    def _where_matches(
        self, record: SearchRecord, expression: str, pythonpath: str | None
    ) -> bool:
        if record.kind == "doc":
            runtime_doc = _RuntimeDocProxy(
                payload=record.payload,
                name=record.doc_name or record.name,
                model_type=self._model_proxy(record),
            )
            return _where_matches(
                runtime_doc,  # type: ignore[arg-type]
                expression,
                self._resolve_model_ref,
                pythonpath,
            )

        if record.kind == "field":
            value = record.value
            data = {
                "value": value,
                "doc": record.doc_name,
                "model": record.model_name,
                "field": record.field_path,
                "path": record.path,
                "owning_section": record.owning_section or "",
            }
            if expression.startswith("has("):
                key = expression[4:-1]
                return key in data and data[key] not in (None, "", [], {})
            for op in ("=", "!="):
                if op in expression:
                    left, right = [part.strip() for part in expression.split(op, 1)]
                    expected = (
                        right[1:-1]
                        if right.startswith('"') and right.endswith('"')
                        else right
                    )
                    actual = data.get(left)
                    return (
                        (str(actual) == expected)
                        if op == "="
                        else (str(actual) != expected)
                    )
            return False

        if record.kind == "section":
            if expression.startswith("title ~ "):
                pattern = expression.split("~", 1)[1].strip().strip('"')
                return re.search(pattern, record.title or "") is not None
            contains_match = re.fullmatch(
                r'"([^"]+)"\s+in\s+(about|breadcrumbs|semantic_tags)', expression
            )
            if contains_match:
                needle, field = contains_match.groups()
                haystack: list[str] = []
                if field == "about":
                    haystack = record.about or []
                elif field == "breadcrumbs":
                    haystack = record.payload.get("breadcrumbs", [])
                elif field == "semantic_tags":
                    haystack = record.semantic
                return needle in haystack
            if expression.startswith("path = "):
                expected = expression.split("=", 1)[1].strip().strip('"')
                return record.path == expected
            return True
        return True

    def _serialize(self, record: SearchRecord) -> dict[str, Any]:
        data = record.as_dict()
        if record.kind == "doc":
            data["semantic_tags"] = list(record.semantic)
        return data

    def _format_line(self, item: dict[str, Any]) -> str:
        parts = [item.get("kind", "?")]
        for key in ("store", "model", "doc", "field", "path", "name"):
            value = item.get(key)
            if value:
                parts.append(str(value))
        if "value" in item and item.get("value") not in (None, ""):
            parts.append(f"value={item['value']}")
        return " | ".join(parts)

    def _model_proxy(self, record: SearchRecord) -> type:
        class _Proxy:
            __module__ = ""

        _Proxy.__name__ = record.model_name or "Model"
        return _Proxy

    @staticmethod
    def _resolve_model_ref(model_ref: str, pythonpath: str | None):
        from sldb.cli.utils import resolve_model_ref

        return resolve_model_ref(model_ref, pythonpath)
