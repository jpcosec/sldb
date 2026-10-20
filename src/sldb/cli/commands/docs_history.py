"""`sldb docs history <doc>`: who signed each committed version, and what moved."""

from __future__ import annotations

from typing import Any

from sldb.api.documents.document_history import document_history
from sldb.cli.output_format import emit


def docs_history(args: Any) -> int:
    entries = document_history(args.store, args.doc, args.pythonpath, since=args.since)
    emit({"doc": args.doc, "entries": entries}, args.format, _text(args.doc, entries))
    return 0


def _text(doc: str, entries: list[dict[str, Any]]) -> str:
    if not entries:
        return f"{doc}: no git history (not a git work tree, or never committed)"
    lines = [f"{doc}: {len(entries)} version(s), newest first"]
    for e in entries:
        signed = f"{e['by']} ({e['authority']})" + ("" if e["declared"] else " [no block]")
        moved = ", ".join(e["changed_fields"]) if e["changed_fields"] else "-"
        lines.append(f"  {e['commit'][:10]}  {e['date']}  {signed}  fields: {moved}")
    return "\n".join(lines)
