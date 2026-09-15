from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.commands.faq_entry import FAQEntry
from sldb.cli.store_context import get_store_context

class FAQCLI:
    """Question-oriented FAQ browser."""

    def run(self, args: Any) -> int:
        entries = self._load_entries(self._faq_path(args))
        question = (args.question or "").strip()
        if not question:
            return self._handle_no_question(args, entries)
        return self._handle_question(args, entries, question)

    def _faq_path(self, args: Any) -> Path:
        path = Path(args.faq_path)
        if path.is_absolute():
            return path
        _store, root = get_store_context(args.store, mode="readonly")
        return root / path

    def _handle_no_question(self, args: Any, entries: list[FAQEntry]) -> int:
        payload = [{"index": e.index, "slug": e.slug, "title": e.title} for e in entries]
        if args.format == "text":
            print("SLDB FAQ questions:")
            for entry in payload:
                print(f"{entry['index']}. {entry['title']} [{entry['slug']}]")
            return 0
        self._print({"questions": payload}, args.format)
        return 0

    def _handle_question(self, args: Any, entries: list[FAQEntry], question: str) -> int:
        entry = self._select_entry(entries, question)
        if entry is None:
            print(f"Unknown FAQ question: {args.question}")
            return 1
        payload = {"index": entry.index, "slug": entry.slug, "title": entry.title, "body": entry.body}
        if args.format == "text":
            print(f"## {entry.title}\n\n{entry.body}")
            return 0
        self._print(payload, args.format)
        return 0

    def _load_entries(self, path: Path) -> list[FAQEntry]:
        text = path.read_text(encoding="utf-8")
        parts = text.split("\n## ")
        return [self._parse_chunk(i, chunk) for i, chunk in enumerate(parts[1:], start=1)]

    def _parse_chunk(self, index: int, chunk: str) -> FAQEntry:
        title, _, body = chunk.partition("\n")
        return FAQEntry(index=index, title=title.strip(), slug=self._slug(title), body=body.strip())

    def _select_entry(self, entries: list[FAQEntry], question: str) -> FAQEntry | None:
        if question.isdigit():
            return next((e for e in entries if e.index == int(question)), None)
        low = question.lower()
        return next((e for e in entries if low == e.slug or low in e.slug or low in e.title.lower()), None)

    def _print(self, payload: dict[str, Any], fmt: str) -> None:
        if fmt == "yaml":
            print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
            return
        print(json.dumps(payload, indent=2))

    def _slug(self, text: str) -> str:
        cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
        while "--" in cleaned:
            cleaned = cleaned.replace("--", "-")
        return cleaned.strip("-") or "question"
