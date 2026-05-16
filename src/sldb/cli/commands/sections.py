from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.graph import (
    _map_fields_to_sections,
    build_document_ir,
    flatten_payload,
    iter_search_records,
    resolve_runtime_doc,
    search_records,
)
from sldb.cli.utils import get_store_context
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_sections_index,
    load_store_index,
)
from sldb.store.models import SectionContextRecord


def _section_record_to_entry(sec: SectionContextRecord) -> dict:
    return {
        "path": sec.path,
        "title": sec.title,
        "breadcrumbs": list(sec.breadcrumbs),
        "about": list(sec.about) if sec.about else [],
        "semantic_tags": list(sec.semantic_tags) if sec.semantic_tags else [],
        "slug": sec.slug,
        "level": sec.level,
        "line_start": sec.line_start,
        "line_end": sec.line_end,
    }


class SectionsCLI:
    """Noun-first section inspection surface."""

    @staticmethod
    def _load_persisted_sections(store_index, root, model_name: str, doc_name: str):
        for model_entry in store_index.models:
            if model_entry.name != model_name:
                continue
            models_idx = load_models_index(root / model_entry.models_index)
            if not models_idx.sections_index:
                return None
            sections_idx = load_sections_index(root / models_idx.sections_index)
            return next(
                (ds for ds in sections_idx.documents if ds.doc_name == doc_name),
                None,
            )
        return None

    def run(self, args: Any) -> int:
        command = args.sections_command
        if command == "show":
            return self._show(args)
        if command == "find":
            return self._find(args)
        if command == "fields":
            return self._fields(args)
        raise SystemExit(f"Unknown sections command: {command}")

    def _show(self, args: Any) -> int:
        runtime_doc = resolve_runtime_doc(args.store, args.doc, args.pythonpath)
        sp, root = get_store_context(args.store)
        store_index = load_store_index(sp)
        doc_sections = self._load_persisted_sections(
            store_index, root, runtime_doc["model"], runtime_doc["name"]
        )
        if doc_sections is not None and doc_sections.sections:
            entries = [_section_record_to_entry(sec) for sec in doc_sections.sections]
        else:
            markdown = Path(runtime_doc["absolute_path"]).read_text(encoding="utf-8")
            ir = build_document_ir(
                runtime_doc, markdown, template=runtime_doc.get("template")
            )
            entries = [entry.model_dump(mode="json") for entry in ir.context_index]
        if args.format == "text":
            for entry in entries:
                bread = " > ".join(entry.get("breadcrumbs", []))
                print(f"{entry['title']}  [{entry['path']}]")
                if bread:
                    print(f"  breadcrumbs: {bread}")
                about = entry.get("about", [])
                if about:
                    print(f"  about: {', '.join(about[:5])}")
                tags = entry.get("semantic_tags", [])
                if tags:
                    print(f"  tags: {', '.join(tags)}")
                print()
        elif args.format == "yaml":
            print(
                yaml.safe_dump(
                    {"sections": entries}, sort_keys=False, allow_unicode=True
                )
            )
        else:
            print(json.dumps({"sections": entries}, indent=2))
        return 0 if entries else 1

    def _find(self, args: Any) -> int:
        records = iter_search_records(
            args.store,
            args.pythonpath,
            include_linked=getattr(args, "global_scope", False),
            rebuild=getattr(args, "rebuild", False),
        )
        matched = search_records(
            records,
            args.term,
            search_in=args.search_in,
            regex=args.regex,
            fuzzy=args.fuzzy,
            kinds={"section"},
        )
        if hasattr(args, "where") and args.where:
            from sldb.cli.commands.find import FindCLI

            find_cli = FindCLI()
            matched = [
                r
                for r in matched
                if find_cli._where_matches(r, args.where, args.pythonpath)
            ]
        payload = [r.as_dict() for r in matched]
        if args.format == "text":
            for item in payload:
                parts = [
                    item.get("title", ""),
                    f"[{item.get('path', '')}]",
                ]
                if item.get("about"):
                    parts.append(f"about={', '.join(item['about'][:3])}")
                print(" | ".join(p.strip() for p in parts if p.strip()))
        elif args.format == "yaml":
            print(
                yaml.safe_dump(
                    {"results": payload}, sort_keys=False, allow_unicode=True
                )
            )
        else:
            print(json.dumps({"results": payload}, indent=2))
        return 0 if payload else 1

    def _fields(self, args: Any) -> int:
        target = args.target
        if not target.startswith("docs/"):
            raise SystemExit("Usage: sldb sections fields docs/<Doc>/<section_path>")
        remainder = target[len("docs/") :]
        parts = remainder.split("/", 1)
        doc_ref = parts[0]
        section_path = parts[1] if len(parts) > 1 else ""

        runtime_doc = resolve_runtime_doc(args.store, doc_ref, args.pythonpath)
        sp, root = get_store_context(args.store)
        store_index = load_store_index(sp)
        doc_sections = self._load_persisted_sections(
            store_index, root, runtime_doc["model"], runtime_doc["name"]
        )
        field_paths = [p for p, _ in flatten_payload(runtime_doc["payload"])]
        if doc_sections is not None and doc_sections.sections:
            template = runtime_doc.get("template") or ""
            owning_map = _map_fields_to_sections(template, doc_sections.sections)
            matched = [
                {
                    "field_path": fp,
                    "value": dict(flatten_payload(runtime_doc["payload"])).get(fp),
                    "owning_section": owning_map.get(fp),
                }
                for fp in field_paths
                if not section_path or owning_map.get(fp) == section_path
            ]
        else:
            markdown = Path(runtime_doc["absolute_path"]).read_text(encoding="utf-8")
            ir = build_document_ir(
                runtime_doc, markdown, template=runtime_doc.get("template")
            )
            matched = [
                node.model_dump(mode="json")
                for node in ir.nodes
                if node.kind == "field"
                and (node.owning_section == section_path or not section_path)
            ]
        if args.format == "text":
            for node in matched:
                print(
                    f"{node['field_path']} = {node.get('value')!r}  [{node.get('owning_section', '?')}]"
                )
        elif args.format == "yaml":
            print(
                yaml.safe_dump({"fields": matched}, sort_keys=False, allow_unicode=True)
            )
        else:
            print(json.dumps({"fields": matched}, indent=2))
        return 0 if matched else 1
