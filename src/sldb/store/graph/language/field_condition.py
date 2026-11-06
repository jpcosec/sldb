"""Deprecated (GO05): one facet-field condition, now a shim over the predicate language.

Constructing a `FieldCondition` emits `DeprecationWarning`; `predicate()` is its translation
to the language (rules-language.md §7, rows 12-19): `eq`/`ne`/`gt`/`lt` are `= != > <`,
`contains` is `"x" in f` (also a substring now), `starts_with` is `f ~ "^x"` (x escaped),
`is_null` is `not has(f)` and `is_not_null` is `has(f)` (`has` also rejects `""`). GO10
retires it.
"""

from __future__ import annotations

import warnings
from typing import Any, Literal

from pydantic import BaseModel, Field, PrivateAttr

from sldb.store.graph.language.field_condition_translation import condition_predicate


class FieldCondition(BaseModel):
    """A single comparison condition on a facet field (deprecated: write the predicate)."""

    field: str = Field(description="Name of the field within the facet.")
    op: Literal["eq", "ne", "is_null", "is_not_null", "contains", "gt", "lt", "starts_with"] = Field(description="The comparison operator.")
    value: Any = Field(default=None, description="The value to compare against; ignored by the null operators.")

    _predicate: Any = PrivateAttr(default=None)

    def model_post_init(self, context: Any) -> None:
        self._predicate = condition_predicate(self.field, self.op, self.value)
        warnings.warn(f"FieldCondition is deprecated: write the predicate `{self._predicate.text}` (rules-language.md)", DeprecationWarning, stacklevel=2)

    def predicate(self) -> Any:
        """The condition in the predicate language (a parsed `Predicate`)."""
        return self._predicate
