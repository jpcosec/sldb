"""A selector asked for one document and several matched; `candidates` names them."""

from __future__ import annotations

from .sldb_document_target_error import SLDBDocumentTargetError


class AmbiguousSelectionError(SLDBDocumentTargetError):
    """`select_documents(..., expect="one")` found more than one document.

    `candidates` holds the export id (`Model:name`, `alias:Model:name` when linked) of each
    match, in the order the selection returns them; the message lists them too.
    """

    def __init__(self, selector: str, candidates: list[str]) -> None:
        self.selector, self.candidates = selector, list(candidates)
        super().__init__(f"Ambiguous selection {selector}: {', '.join(self.candidates)}")
