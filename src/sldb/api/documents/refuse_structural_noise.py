"""The refusal every path that writes a new document goes through.

`docs track` and `docs create` reach this; it raises rather than warning, so a
document whose headings the model does not declare never enters the store, unless the
store's policy (or sldb's default for a narrative or `authored` model) allows that noise
(docs/architecture/provenance.md §5).
"""

from __future__ import annotations

from typing import Any

from sldb.api.documents.structural_noise import find_structural_noise
from sldb.core.exceptions import SLDBValidationError


def refuse_structural_noise(model_type: type, markdown: str, name: str, policy: Any = None) -> None:
    """Raise unless every heading in `markdown` is declared by the model's template, or the
    policy allows the noise for this model.

    Args:
        model_type: The `StructuredNLDoc` subclass the document is tracked as.
        markdown: The document's Markdown source.
        name: Document name, used in the message.
        policy: The store's `Policy`; sldb's defaults when None.

    Raises:
        SLDBValidationError: When the document carries undeclared headings; the message
            names them and points at a child model declaring them as `optrev` fields.
    """
    from sldb.api.stores.policy import Policy, Subject
    from sldb.models.provenance import Provenance

    report = find_structural_noise(model_type, markdown, name)
    authority, declared = Provenance.of_model(model_type)
    subject = Subject(authority=authority, declared=declared, narrative=report.narrative)
    if report.clean or (policy or Policy()).response("structural-noise", report.model, subject) in ("allow", "ignore"):
        return
    raise SLDBValidationError(report.message(), report.details())
