"""The invariants of one composed `ViewDoc` (GD25) that cross its own fields: unique param
names and section keys, selectors with known keys and parseable `where`, every `{param}` a
section references declared, and the name `projection` kept for the `/views/projection*`
routes. Whether a rule names an existing RuleDoc depends on the store: `run_view` checks it."""

from __future__ import annotations

import re
from typing import Any

RESERVED_NAMES = ("projection",)
SELECTOR_KEYS = ("ref", "prefix", "path_glob", "model", "where", "include_linked")
PLACEHOLDER = re.compile(r"\{([A-Za-z_]\w*)\}")


def check_view_name(name: str) -> None:
    if name in RESERVED_NAMES:
        raise ValueError(f"view name {name!r} is reserved")


def check_params(params: list[Any]) -> None:
    names = [param.name for param in params]
    repeated = sorted({name for name in names if names.count(name) > 1})
    if repeated:
        raise ValueError(f"params declared more than once: {repeated}")


def check_sections(sections: list[Any], params: list[Any]) -> None:
    keys = [section.key for section in sections]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise ValueError(f"section keys declared more than once: {repeated}")
    declared = {param.name for param in params}
    for section in sections:
        check_select(section.key, section.select)
        unknown = sorted(placeholders(section.select) - declared)
        if unknown:
            raise ValueError(f"section {section.key!r} references undeclared params: {unknown}")


def check_select(key: str, select: dict[str, Any]) -> None:
    """The selector's keys are `select_documents`'s, its strings are not blank, `where` parses."""
    unknown = sorted(set(select) - set(SELECTOR_KEYS))
    if unknown:
        raise ValueError(f"section {key!r}: unknown selector keys {unknown}")
    for name, value in select.items():
        if name == "include_linked" and not isinstance(value, bool):
            raise ValueError(f"section {key!r}: include_linked must be a boolean")
        if name != "include_linked" and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"section {key!r}: selector key {name} must be a non-blank string")
    if select.get("where"):
        _parse(key, select["where"])


def placeholders(select: dict[str, Any]) -> set[str]:
    """The `{param}` names the selector's string values reference."""
    return {name for value in select.values() if isinstance(value, str) for name in PLACEHOLDER.findall(value)}


def _parse(key: str, text: str) -> None:
    from sldb.store.graph.language.predicate_parser import parse_predicate

    try:
        parse_predicate(text)
    except ValueError as exc:
        raise ValueError(f"section {key!r}: where does not parse: {exc}") from exc
