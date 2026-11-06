"""The class attribute lines of a generated model: family, semantics, template and metadata."""

from __future__ import annotations

import json
from typing import Any

import yaml

_PLAIN = ("family", "authority")


def class_attr_lines(spec: dict[str, Any], template: str, args: Any = None) -> list[str]:
    """`__family__` ... `__compositions__` lines, the `__template__` between semantics and containment."""
    head = _lines(("family", "authority", "semantics"), spec, args)
    tail = _lines(("containment", "references", "compositions"), spec, args)
    return head + [f"    __template__ = {template!r}"] + tail


def _lines(names: tuple[str, ...], spec: dict[str, Any], args: Any) -> list[str]:
    """One assignment per attribute that has a value from the CLI option or the spec."""
    values = ((name, _value(name, spec, args)) for name in names)
    return [f"    __{name}__ = {value!r}" for name, value in values if value is not None]


def _value(name: str, spec: dict[str, Any], args: Any) -> Any:
    """The CLI option wins; text options (but family and authority) parse as JSON or YAML."""
    value = getattr(args, name, None) if args else None
    if value is None:
        return spec.get(name)
    return _parse(value) if isinstance(value, str) and name not in _PLAIN else value


def _parse(text: str) -> Any:
    """JSON when it starts like a mapping or list, YAML otherwise."""
    return json.loads(text) if text.startswith(("{", "[")) else yaml.safe_load(text)
