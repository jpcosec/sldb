"""A symbol document's purpose, generated from its docstring without overwriting what was written.

Spec section 2: the first body paragraph of the docstring supplies the generated purpose,
verbatim after whitespace normalization. Section 7: an authored purpose is never silently
overwritten; a difference is reported for an explicit decision. A purpose still equal to what
the previous docstring generated is not authored, and follows the docstring.
"""

from __future__ import annotations

import re

PLACEHOLDER = "Not documented."


def first_paragraph(docstring: str | None) -> str | None:
    """The docstring body's first paragraph, whitespace-normalized; None when there is none."""
    from .docstring_metadata import parse_docstring

    body = parse_docstring(None if docstring in (None, PLACEHOLDER) else docstring).body
    paragraph = body.split("\n\n", 1)[0] if body else ""
    return re.sub(r"\s+", " ", paragraph).strip() or None


def merged_purpose(current: str | None, previous_docstring: str | None, docstring: str | None) -> str:
    """The purpose to write: generated when the current one is a placeholder or was generated."""
    generated = first_paragraph(docstring)
    if generated is None or current == generated:
        return current or PLACEHOLDER
    if current in (None, "", PLACEHOLDER) or current == first_paragraph(previous_docstring):
        return generated
    return current  # authored: kept, and reported by `purpose_conflict`


def purpose_conflict(purpose: str, docstring: str | None) -> bool:
    """An authored purpose that differs from what the docstring now says."""
    generated = first_paragraph(docstring)
    return generated is not None and purpose not in (PLACEHOLDER, generated)
