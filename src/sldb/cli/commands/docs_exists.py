"""`sldb docs exists REF`: CLI adapter over `sldb.api.stores.doc_status`.

The exit code carries the answer so callers need not parse text: 0 ok, 1 missing,
2 ambiguous, 5 link-missing or link-broken (the reference cannot be checked here).
"""
from __future__ import annotations
import json
from typing import Any
from sldb.api.stores.doc_status import doc_status

EXIT_CODES = {"ok": 0, "missing": 1, "ambiguous": 2, "link-missing": 5, "link-broken": 5}


def docs_exists(args: Any) -> int:
    status = doc_status(args.store, args.ref)
    if args.format == "json":
        print(json.dumps(status.model_dump(exclude_none=True)))
    else:
        print(_text_line(status))
    return EXIT_CODES[status.status]


def _text_line(status: Any) -> str:
    if status.exists:
        return f"ok: {status.store}:{status.model}/{status.name} -> {status.path}"
    return f"{status.status}: {status.ref}" + (f" ({status.detail})" if status.detail else "")
