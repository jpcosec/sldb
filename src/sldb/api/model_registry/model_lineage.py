"""What a model class declares about its place in the model hierarchy.

Moved here from `sldb.cli.commands.model_add`, which re-exports these names.
"""

from __future__ import annotations

from sldb.models.structured_doc import StructuredNLDoc


def model_family(model_type: type) -> str | None:
    """The model's declared `__family__`, the root branch it belongs to.

    Args:
        model_type: The model class.

    Returns:
        The family name, or None when the model declares none.
    """
    value = getattr(model_type, "__family__", None)
    return str(value) if value else None


def model_base_names(model_type: type) -> list[str]:
    """Names of the StructuredNLDoc bases above this model, nearest first.

    Recorded so `st.{Base+}` families and `model <= Base` filters are legible from the
    store index without importing the class.

    Args:
        model_type: The model class.

    Returns:
        Base class names, excluding StructuredNLDoc itself.
    """
    return [
        base.__name__ for base in model_type.__mro__[1:]
        if isinstance(base, type) and issubclass(base, StructuredNLDoc) and base is not StructuredNLDoc
    ]
