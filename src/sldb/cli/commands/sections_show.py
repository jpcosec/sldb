from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import yaml
from sldb.cli.graph_ops import build_document_ir, resolve_runtime_doc
from sldb.cli.store_context import get_store_context
from sldb.store.io import load_store_index
from sldb.store.source_read import read_source_text
from sldb.cli.commands.sections_common import load_persisted_sections, section_record_to_entry

class ShowSectionsCLI:
    def run(self, args: Any) -> int:
        entries = self._get_show_entries(args)
        return self._format_show_entries(entries, args.format)

    def _get_show_entries(self, args: Any) -> list[dict]:
        runtime_doc = resolve_runtime_doc(args.store, args.doc, args.pythonpath)
        sp, root = get_store_context(args.store)
        doc_sections = load_persisted_sections(
            load_store_index(sp), root, runtime_doc["model"], runtime_doc["name"]
        )
        if doc_sections is not None and doc_sections.sections:
            return [section_record_to_entry(sec) for sec in doc_sections.sections]
        return self._build_ir_entries(runtime_doc)

    def _build_ir_entries(self, runtime_doc: dict) -> list[dict]:
        markdown = read_source_text(Path(runtime_doc["absolute_path"]))
        ir = build_document_ir(runtime_doc, markdown, template=runtime_doc.get("template"))
        return [entry.model_dump(mode="json") for entry in ir.context_index]

    def _format_show_entries(self, entries: list[dict], fmt: str) -> int:
        if fmt == "text":
            self._print_show_text(entries)
        elif fmt == "yaml":
            print(yaml.safe_dump({"sections": entries}, sort_keys=False, allow_unicode=True))
        else:
            print(json.dumps({"sections": entries}, indent=2))
        return 0 if entries else 1

    def _print_show_text(self, entries: list[dict]) -> None:
        for entry in entries:
            self._print_single_show_entry(entry)

    def _print_single_show_entry(self, entry: dict) -> None:
        bread = " > ".join(entry.get("breadcrumbs", []))
        print(f"{entry['title']}  [{entry['path']}]")
        if bread:
            print(f"  breadcrumbs: {bread}")
        if about := entry.get("about", []):
            print(f"  about: {', '.join(about[:5])}")
        if tags := entry.get("semantic_tags", []):
            print(f"  tags: {', '.join(tags)}")
        print()
