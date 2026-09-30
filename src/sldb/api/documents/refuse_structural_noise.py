"""The refusal every path that writes a new document goes through.

`docs track` and `docs create` reach this; it raises rather than warning, so a
document whose headings the model does not declare never enters the store.
"""

from __future__ import annotations

from sldb.api.documents.structural_noise import find_structural_noise
from sldb.core.exceptions import SLDBValidationError


def refuse_structural_noise(model_type: type, markdown: str, name: str) -> None:
    """Raise unless every heading in `markdown` is declared by the model's template.

    Args:
        model_type: The `StructuredNLDoc` subclass the document is tracked as.
        markdown: The document's Markdown source.
        name: Document name, used in the message.

    Raises:
        SLDBValidationError: When the document carries undeclared headings; the message
            names them and points at a child model declaring them as `optrev` fields.
    """
    report = find_structural_noise(model_type, markdown, name)
    if report.clean:
        return
    raise SLDBValidationError(report.message(), report.details())
