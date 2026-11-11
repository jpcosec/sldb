from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import yaml
from sldb.cli.graph_ops import _map_fields_to_sections, build_document_ir, flatten_payload, resolve_runtime_doc
from sldb.cli.store_context import get_store_context
from sldb.store.io import load_store_index
from sldb.store.source_read import read_source_text
from sldb.cli.commands.sections_common import load_persisted_sections

class FieldsSectionsCLI:
    def run(self, args: Any) -> int:
        doc_ref, section_path = self._parse_fields_target(args.target)
        matched = self._get_fields_matches(args, doc_ref, section_path)
        return self._format_fields_matches(matched, args.format)

    def _parse_fields_target(self, target: str) -> tuple[str, str]:
        if not target.startswith("docs/"):
            raise SystemExit("Usage: sldb sections fields docs/<Doc>/<section_path>")
        parts = target[len("docs/") :].split("/", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""

    def _get_fields_matches(self, args: Any, doc_ref: str, section_path: str) -> list[dict]:
        runtime_doc = resolve_runtime_doc(args.store, doc_ref, args.pythonpath)
        sp, root = get_store_context(args.store)
        doc_sections = load_persisted_sections(
            load_store_index(sp), root, runtime_doc["model"], runtime_doc["name"]
        )
        if doc_sections is not None and doc_sections.sections:
            return self._match_persisted_fields(runtime_doc, doc_sections.sections, section_path)
        return self._match_ir_fields(runtime_doc, section_path)

    def _match_persisted_fields(self, runtime_doc: dict, sections: list, section_path: str) -> list[dict]:
        template = runtime_doc.get("template") or ""
        owning_map = _map_fields_to_sections(template, sections)
        payload_dict = dict(flatten_payload(runtime_doc["payload"]))
        return [
            {"field_path": fp, "value": payload_dict.get(fp), "owning_section": owning_map.get(fp)}
            for fp, _ in flatten_payload(runtime_doc["payload"])
            if not section_path or owning_map.get(fp) == section_path
        ]

    def _match_ir_fields(self, runtime_doc: dict, section_path: str) -> list[dict]:
        markdown = read_source_text(Path(runtime_doc["absolute_path"]))
        ir = build_document_ir(runtime_doc, markdown, template=runtime_doc.get("template"))
        return [
            node.model_dump(mode="json") for node in ir.nodes
            if node.kind == "field" and (node.owning_section == section_path or not section_path)
        ]

    def _format_fields_matches(self, matched: list[dict], fmt: str) -> int:
        if fmt == "text":
            self._print_fields_text(matched)
        elif fmt == "yaml":
            print(yaml.safe_dump({"fields": matched}, sort_keys=False, allow_unicode=True))
        else:
            print(json.dumps({"fields": matched}, indent=2))
        return 0 if matched else 1

    def _print_fields_text(self, matched: list[dict]) -> None:
        for node in matched:
            print(f"{node['field_path']} = {node.get('value')!r}  [{node.get('owning_section', '?')}]")
