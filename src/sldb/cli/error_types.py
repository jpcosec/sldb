"""The typed error of an enveloped CLI run: `ns/name` and the exit code it maps to.

0 ok · 1 something named is missing · 2 a selector is ambiguous · 3 the input is rejected ·
4 conflict, stale or busy · 5 the store or the runtime failed · 6 usage · 70 unexpected.
A command that runs and reports findings (`stores check` FAIL) is `<group>/failed` with the
command's own exit code. Only the `--envelope` mode uses this table; the plain CLI keeps its
exit codes, which callers read today.
"""

from __future__ import annotations

from sldb.core.exceptions import (
    SLDBASTError,
    SLDBDocumentTargetError,
    SLDBError,
    SLDBFieldPathError,
    SLDBGraphArgumentError,
    SLDBGraphCycleError,
    SLDBLinkError,
    SLDBModelError,
    SLDBPayloadSaveError,
    SLDBStoreError,
    SLDBValidationError,
)

EXIT_CODES = {"ok": 0, "missing": 1, "ambiguous": 2, "rejected": 3, "conflict": 4, "runtime": 5, "usage": 6, "unexpected": 70}

_BY_CLASS = (
    (SLDBFieldPathError, "fields", "missing"),
    (SLDBLinkError, "links", "missing"),
    (SLDBModelError, "models", "rejected"),
    (SLDBValidationError, "validate", "rejected"),
    (SLDBPayloadSaveError, "docs", "rejected"),
    (SLDBGraphArgumentError, "graph", "rejected"),
    (SLDBGraphCycleError, "graph", "rejected"),
    (SLDBASTError, "markdown", "runtime"),
)


def error_type(exc: BaseException) -> tuple[str, int]:
    """`(ns/name, exit)` for an exception raised by a command."""
    special = _special(exc)
    if special:
        return special
    for cls, ns, kind in _BY_CLASS:
        if isinstance(exc, cls):
            return f"{ns}/{kind}", EXIT_CODES[kind]
    return ("sldb/error", EXIT_CODES["runtime"]) if isinstance(exc, SLDBError) else ("cli/unexpected", EXIT_CODES["unexpected"])


def _special(exc: BaseException) -> tuple[str, int] | None:
    text = str(exc).lower()
    if isinstance(exc, SLDBDocumentTargetError):
        kind = "ambiguous" if "ambiguous" in text else "missing"
        return f"docs/{kind}", EXIT_CODES[kind]
    if isinstance(exc, SLDBStoreError):
        return ("store/busy", EXIT_CODES["conflict"]) if "busy" in text else ("store/error", EXIT_CODES["runtime"])
    if isinstance(exc, FileNotFoundError):
        return "io/missing", EXIT_CODES["missing"]
    return None
