"""What the store reads from a model class and from sldb's built-in vocabulary: the one seam.

The store is a typed-document engine that sldb's document models feed. Everything it needs to
know about them (a class's document bases, its declared family, how a field is described, the
relation types sldb ships) comes through here, so the store's other modules import nothing
from `sldb.models` directly, and a store packaged on its own replaces only this module
(task: desacoplar el store dentro de sldb). Imports are lazy where the store's import time
must not pull the document models in.
"""

from __future__ import annotations

from typing import Any

from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_payload  # noqa: F401 - plain data


def base_names(model_type: Any) -> list[str]:
    """Names of the document-model bases above this model, nearest first (not the root class)."""
    from sldb.models.structured_doc import StructuredNLDoc

    return [b.__name__ for b in model_type.__mro__[1:] if isinstance(b, type) and issubclass(b, StructuredNLDoc) and b is not StructuredNLDoc]


def declared_family(model_type: Any) -> str | None:
    """The class's `__family__`, the root branch it belongs to; None when it declares none."""
    value = getattr(model_type, "__family__", None)
    return str(value) if value else None


def describe_field(name: str, field: Any) -> Any:
    """How one field is described for the field nodes of the edge index."""
    from sldb.models.field_schema.describe import describe_field as describe

    return describe(name, field)
