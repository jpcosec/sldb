"""The per-kind checks of `sldb notations validate`, and how a file or a name is told apart."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import yaml

from sldb.core.finding import Finding, alert

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


def _ambiguity(target: str, kinds: list[str]) -> list[Finding]:
    if len(kinds) < 2 or Path(target).is_file():
        return []
    return [alert("notations/ambiguous-name", target, f"{target!r} exists as {' and '.join(kinds)}; validating the {kinds[0]}", "pass a path to validate the other one")]
