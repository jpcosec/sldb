"""`sldb notations validate <name|path>`: validate a notation, a palette or a spec; print findings."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

import yaml

from sldb.core.finding import Finding, alert, error

Check = Callable[[str], None]


def _check_notation(target: str) -> None:
    from sldb.notations.notation_files import load_notation

    load_notation(target)


def _check_palette(target: str) -> None:
    from sldb.notations.palette_checks import check_palette
    from sldb.notations.palette_files import load_palette

    check_palette(load_palette(target))


def _check_spec(target: str) -> None:
    from sldb.api.notations.spec_models import load_spec, validate_spec

    validate_spec(load_spec(target))


_CHECKS: dict[str, Check] = {"notation": _check_notation, "palette": _check_palette, "spec": _check_spec}


def _root_keys(path: Path) -> set[str]:
    """Root keys of a YAML/JSON file (JSON is YAML); empty if unreadable or not a mapping."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError, UnicodeDecodeError):
        return set()
    return set(raw) if isinstance(raw, dict) else set()


def _kinds_of_file(path: Path) -> list[str]:
    keys = _root_keys(path)
    if keys & {"palette", "colors"}:
        return ["palette"]
    if "type" in keys:
        return ["spec"]
    return ["notation"]


def _store_names(store: str | None, model: str) -> set[str]:
    if not store:
        return set()
    import sldb.api as api

    try:
        docs = api.load_runtime_documents(Path(store), None, include_linked=False)
    except Exception:
        return set()
    return {str(d.name) for d in docs if str(d.model_name) == model}


def _kinds_of_name(name: str, store: str | None) -> list[str]:
    from sldb.notations.notation_files import builtin_notations
    from sldb.notations.palette_files import builtin_palettes

    kinds = []
    if name in _store_names(store, "NotationDoc") or name in builtin_notations():
        kinds.append("notation")
    if name in _store_names(store, "PaletteDoc") or name in builtin_palettes():
        kinds.append("palette")
    return kinds


def _run_check(kind: str, target: str) -> Finding | None:
    try:
        _CHECKS[kind](target)
    except Exception as exc:  # every loader raises its own typed error; each one is a finding
        return error(f"notations/{kind}-invalid", target, str(exc))
    return None


def validate_target(target: str, store: str | None = None) -> tuple[list[Finding], bool]:
    """`(findings, known)`; `known` is False when the target is neither a file nor a known name."""
    path = Path(target)
    if path.is_file() and path.suffix.lower() in (".json", ".yml", ".yaml"):
        kinds = _kinds_of_file(path)
    else:
        kinds = _kinds_of_name(target, store)
    if not kinds:
        return [], False
    findings: list[Finding] = []
    if len(kinds) > 1 and not path.is_file():
        findings.append(alert("notations/ambiguous-name", target, f"{target!r} exists as {' and '.join(kinds)}; validating the {kinds[0]}", "pass a path to validate the other one"))
    found = _run_check(kinds[0], target)
    if found:
        findings.append(found)
    return findings, True


def validate(args: Any) -> int:
    """Print the findings (text, or JSON with --json); exit 0, 1 on errors, 2 on an unknown target."""
    from sldb.cli import alert_sink

    findings, known = validate_target(args.target, args.store)
    if not known:
        print(f"unknown notation, palette or spec: {args.target}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps([f.as_dict() for f in findings], indent=2, ensure_ascii=False))
    alert_sink.report(findings, text=not args.json)
    return 1 if any(f.level == "error" for f in findings) else 0
