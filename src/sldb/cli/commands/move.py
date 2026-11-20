"""`sldb move SOURCE DESTINATION`: CLI adapter over `sldb.api.move_path`."""
from __future__ import annotations

import json
from typing import Any

from sldb.api.documents.move_path import move_path


class MoveCLI:
    """Move a file or directory and fix the store's fields and the Markdown links that name it."""

    def run(self, args: Any) -> int:
        report = move_path(args.store, args.source, args.destination, dry_run=args.dry_run, pythonpath=args.pythonpath)
        if args.format == "json":
            print(json.dumps(report.to_dict(), ensure_ascii=False))
        else:
            print("\n".join(_lines(report)))
        return 0


def _lines(report: Any) -> list[str]:
    verb = "Would move" if report.dry_run else "Moved"
    lines = [f"{verb} {report.source} -> {report.destination} ({len(report.moves)} file(s))"]
    lines += [f"  {m['source']} -> {m['destination']}" for m in report.moves]
    lines += [f"  field {c['document']} {c['field']}: {c['old']} -> {c['new']}" for c in report.fields]
    lines += [f"  link {c['file']}:{c['line']}: {c['old']} -> {c['new']}" for c in report.links]
    return lines
