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


def indexed_fields(model_type: Any) -> list[str] | None:
    """The class's `__indexed__` names, checked; None when it declares none.

    Raises:
        SLDBModelError: A name is not a field of the model (own or inherited), or the field's
            declared type is neither a scalar nor a list of scalars.
    """
    names = getattr(model_type, "__indexed__", None)
    if names is None:
        return None
    for name in names:
        _check_indexed(model_type, name)
    return sorted(set(names))


def projected_fields(model_type: Any) -> list[str]:
    """Fields a payload filter may name: `__indexed__`, else every field whose declared type can
    hold a scalar or a list of scalars (`Any` included: known per value). [] without a class."""
    from sldb.store.edge_index.payload_types import opaque_annotation, projectable_annotation

    if model_type is None:
        return []
    indexed = indexed_fields(model_type)
    if indexed is not None:
        return indexed
    return sorted(n for n, f in model_type.model_fields.items() if projectable_annotation(f.annotation) or opaque_annotation(f.annotation))


def contract_signature(model_type: Any) -> str:
    """sha256 of the canonical JSON (sorted keys, UTF-8, no spaces) of the model's field names
    (inherited included) and its `__references__`, `__containment__`, `__compositions__` names;
    "" when the class could not be loaded."""
    import hashlib
    import json

    if model_type is None:
        return ""
    body = {"fields": sorted(model_type.model_fields), **{attr: sorted(getattr(model_type, f"__{attr}__", None) or []) for attr in _DECLARED}}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


_DECLARED = ("references", "containment", "compositions")


def _check_indexed(model_type: Any, name: str) -> None:
    from sldb.store.edge_index.payload_types import projectable_annotation
    from sldb.store.exceptions import SLDBModelError

    field = model_type.model_fields.get(name)
    if field is None:
        raise SLDBModelError(f"Model '{model_type.__name__}': __indexed__ names '{name}', which is not one of its fields.")
    if not projectable_annotation(field.annotation):
        raise SLDBModelError(f"Model '{model_type.__name__}': __indexed__ field '{name}' is declared {field.annotation!r}, not a scalar or a list of scalars.")
