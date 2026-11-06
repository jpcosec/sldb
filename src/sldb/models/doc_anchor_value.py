"""The form of a document anchor (docs/architecture/anchoring.md §6): `doc:Model:name`, or pinned
`doc:Model:name@sha256:<64 hex>` with the contract hash it saw (rules-language.md §5).

The form is a property of one value, so it is checked by the model's own validators: the fields
a model names in `__doc_anchors__` (`StructuredNLDoc`) and the `doc:` items of `Provenance.from_`.
Whether the target exists, its hash now and the anchor's state depend on other documents: the
save pins them and `check_doc_anchors` reports them. What a model definition may declare
(`definition_problems`) is checked when the class is loaded (`store/model_contract.py`).
"""

from __future__ import annotations

import re
import types
from typing import Any, Union, get_args, get_origin

PREFIX = "doc:"
STATE_SUFFIX = "__anchor_state"
_FORM = re.compile(r"doc:([^:@\s]+):([^@\s]+)(?:@sha256:([0-9a-fA-F]{64}))?")


def parse_doc_anchor(value: str) -> tuple[str, str | None] | None:
    """(target export id `Model:name`, seen hash or None) of a well-formed anchor; else None."""
    found = _FORM.fullmatch(value.strip())
    if found is None:
        return None
    return f"{found[1]}:{found[2]}", found[3].lower() if found[3] else None


def check_doc_anchor(value: str, where: str) -> str:
    """`value` when it has the anchor form; ValueError naming `where` and the reason otherwise."""
    if parse_doc_anchor(value) is None:
        raise ValueError(f"{where}: {value!r} is not a document anchor: expected `doc:Model:name` or `doc:Model:name@sha256:<64 hex>`")
    return value


def pinned(value: str, current: str | None) -> str:
    """`value` with `@sha256:<current>` when it carries no hash and the target's hash is known."""
    parsed = parse_doc_anchor(value)
    if parsed is None or parsed[1] is not None or current is None:
        return value
    return f"{value.strip()}@sha256:{current}"


def anchor_items(value: Any) -> list[str]:
    """The non-empty strings a str or list[str] field holds."""
    raw = value if isinstance(value, list) else [value]
    return [item for item in raw if isinstance(item, str) and item.strip()]


def check_anchor_fields(doc: Any) -> Any:
    """The `model_validator` body: every value of every `__doc_anchors__` field has the form."""
    for name in getattr(type(doc), "__doc_anchors__", None) or []:
        for item in anchor_items(getattr(doc, name, None)):
            check_doc_anchor(item, f"field '{name}'")
    return doc


def check_from_items(items: list[str]) -> list[str]:
    """`Provenance.from_` validator: a `doc:` item has the anchor form; any other is left alone."""
    for item in items:
        if isinstance(item, str) and item.strip().startswith(PREFIX):
            check_doc_anchor(item, "from")
    return items


def definition_problems(model_type: Any) -> list[str]:
    """What a model class declares wrongly about anchors: a field with the reserved suffix, an
    `__doc_anchors__` name that is not a field, or a field that is not str or list[str]."""
    fields = model_type.model_fields
    reserved = [f"field '{n}' ends in the reserved suffix '{STATE_SUFFIX}'" for n in fields if n.endswith(STATE_SUFFIX)]
    named = getattr(model_type, "__doc_anchors__", None) or []
    return reserved + [problem for n in named if (problem := _field_problem(fields, n))]


def _field_problem(fields: dict[str, Any], name: str) -> str | None:
    if name not in fields:
        return f"__doc_anchors__ names '{name}', which is not one of its fields"
    if not _str_or_str_list(fields[name].annotation):
        return f"__doc_anchors__ field '{name}' is declared {fields[name].annotation!r}, not str or list[str]"
    return None


def _str_or_str_list(annotation: Any) -> bool:
    """str or list[str], optional (`| None`) or not."""
    args = [a for a in get_args(annotation) if a is not type(None)] if get_origin(annotation) in (Union, types.UnionType) else [annotation]
    if len(args) != 1:
        return False
    return args[0] is str or (get_origin(args[0]) is list and get_args(args[0]) == (str,))
