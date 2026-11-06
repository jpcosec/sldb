"""`sldb docs replace REF --old OLD --new NEW [--count N]`: CLI adapter over `sldb.api.replace_text`.

The JSON (and the envelope's `data`) is what the function returns: `{ref, path, tracked, model,
name, count}`. A count that does not match, a document that no longer validates or an
`on_write` rule that refuses the write leave the file as it was and exit through the envelope's
typed error (`validate/rejected`, `rules/violation`).
"""

from __future__ import annotations

from typing import Any

from sldb.api.documents.replace_text import replace_text
from sldb.cli.output_format import emit


def docs_replace(args: Any) -> int:
    result = replace_text(args.store, args.ref, args.old, args.new, count=args.count, pythonpath=args.pythonpath)
    what = f"{result['model']}:{result['name']}" if result["tracked"] else result["path"]
    emit(result, args.format, f"replaced {result['count']} occurrence(s) in {what} ({result['path']})")
    return 0
