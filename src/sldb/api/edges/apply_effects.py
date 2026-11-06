"""Apply an edge's effects to a subject, purely: the new payload, validated, never persisted."""

from __future__ import annotations

import copy
from typing import Any

from sldb.models.structured_doc import StructuredNLDoc
from sldb.models.transition_attributes import check_sets


def apply_effects(subject: dict[str, Any], effects: dict[str, Any], model: type[StructuredNLDoc]) -> dict[str, Any]:
    """A copy of `subject` where each key of `effects["sets"]` replaces (or adds) the top-level key.

    No nested merge. The whole result is validated against `model` (the subject's model class;
    a caller holding only `Model:name` resolves it with the store's model resolver first).

    Raises:
        ValueError: A value of `sets` is a map or a nested list.
        pydantic.ValidationError: The resulting payload does not validate against `model`.
    """
    sets = (effects or {}).get("sets") or {}
    check_sets(sets)
    payload = {**copy.deepcopy(subject), **copy.deepcopy(sets)}
    model.model_validate(payload)
    return payload
