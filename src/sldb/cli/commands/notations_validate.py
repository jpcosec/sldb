"""`sldb notations validate <name|path>`: validate a notation, a palette or a spec; print findings."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from sldb.cli.commands.notations_validate_store import _STORE_MODELS, _check_store_document, _store_has
from sldb.cli.commands.notations_validate_checks import _CHECKS, _ambiguity, _kinds_of_file
from sldb.core.finding import Finding, error

def _kinds_of_name(name: str, store: str | None) -> list[str]:
    from sldb.notations.notation_files import builtin_notations
    from sldb.notations.palette_files import builtin_palettes

    kinds = []
    if _store_has(store, "notation", name) or name in builtin_notations():
        kinds.append("notation")
    if _store_has(store, "palette", name) or name in builtin_palettes():
        kinds.append("palette")
    return kinds


def _run_check(kind: str, target: str, store: str | None = None) -> Finding | None:
    try:
        if kind in _STORE_MODELS and _store_has(store, kind, target) and not _builtin_or_file(kind, target):
            _check_store_document(kind, target, str(store))
        else:
            _CHECKS[kind](target)
    except Exception as exc:  # every loader raises its own typed error; each one is a finding
        return error(f"notations/{kind}-invalid", target, str(exc))
    return None


def _builtin_or_file(kind: str, target: str) -> bool:
    from sldb.notations.notation_files import builtin_notations
    from sldb.notations.palette_files import builtin_palettes

    if Path(target).is_file():
        return True
    return target in (builtin_notations() if kind == "notation" else builtin_palettes())


def _file_or_name_kinds(target: str, store: str | None) -> list[str]:
    path = Path(target)
    if path.is_file() and path.suffix.lower() in (".json", ".yml", ".yaml"):
        return _kinds_of_file(path)
    return _kinds_of_name(target, store)


def validate_target(target: str, store: str | None = None) -> tuple[list[Finding], bool]:
    """`(findings, known)`; `known` is False when the target is neither a file nor a known name."""
    kinds = _file_or_name_kinds(target, store)
    if not kinds:
        return [], False
    found = _run_check(kinds[0], target, store)
    return _ambiguity(target, kinds) + ([found] if found else []), True


def _declared_standard(target: str, store: str | None) -> dict[str, Any] | None:
    if _builtin_or_file("notation", target):
        from sldb.notations.notation_files import load_notation

        std = load_notation(target).standard
        return std.model_dump() if std else None
    from sldb.api.notations.notation_listing import notation_standards

    return notation_standards(store or ".", None).get(f"NotationDoc:{target}")


def _standard_shown(target: str, store: str | None, findings: list[Finding]) -> dict[str, Any] | None:
    """The `{name, version}` a valid notation declares, else None (no field, not a notation, or invalid)."""
    if any(f.level == "error" for f in findings) or "notation" not in _file_or_name_kinds(target, store):
        return None
    try:
        return _declared_standard(target, store)
    except Exception:
        return None


def _print_json(findings: list[Finding], standard: dict[str, Any] | None) -> None:
    listed = [f.as_dict() for f in findings]
    print(json.dumps({"findings": listed, "standard": standard} if standard else listed, indent=2, ensure_ascii=False))


def _report(args: Any, findings: list[Finding]) -> None:
    from sldb.cli import alert_sink

    standard = _standard_shown(args.target, args.store, findings)
    if args.json:
        _print_json(findings, standard)
    alert_sink.report(findings, text=not args.json)
    if standard and not args.json:
        print(f"standard: {standard['name']}" + (f" {standard['version']}" if standard.get("version") else ""))


def validate(args: Any) -> int:
    """Print the findings (text, or JSON with --json); exit 0, 1 on errors, 2 on an unknown target."""
    findings, known = validate_target(args.target, args.store)
    if not known:
        print(f"unknown notation, palette or spec: {args.target}", file=sys.stderr)
        return 2
    _report(args, findings)
    return 1 if any(f.level == "error" for f in findings) else 0
