"""A facet payload: attribute-addressable extra fields, without an ontology dependency."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class FacetPayload(BaseModel):
    """Extra facet fields, addressable by attribute with lazy defaults."""

    model_config = ConfigDict(extra="allow")
    _DEFAULTS: ClassVar[dict[str, object]] = {
        "compiled_from": "wiki-compiler",
        "coverage_percent": None,
        "direction": "input",
        "exemption_reason": None,
        "failing_standards": list,
        "raw_docstring": None,
    }

    def __getattr__(self, name: str) -> object:
        extra = self.model_extra or {}
        if name in extra:
            return extra[name]
        defaults = type(self)._DEFAULTS
        if name not in defaults:
            raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")
        value = defaults[name]
        resolved = value() if callable(value) else value
        extra[name] = resolved
        return resolved
