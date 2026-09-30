"""Find the headings a document carries that its model's `__template__` never declares.

A heading inside a field is a field the model is missing, not prose: SLDB takes
text apart into propositions with no structural noise left over. This module is
the detection; the refusal lives in the write paths that call it.
"""

from __future__ import annotations

from sldb.api.documents.heading_scan import is_wildcard, scan_headings
from sldb.api.documents.structural_noise_report import StructuralNoiseReport


def declared_headings(template: str) -> tuple[set[tuple[int, str]], set[int]]:
    """The literal heading slots a template declares, and the levels it leaves open.

    Args:
        template: A model's `__template__`.

    Returns:
        `(literals, wildcard_levels)`; a heading whose title is a marker (`⸢rev•title⸥`)
        declares its whole level open, since the rendered title comes from a field.
    """
    literals, wildcards = set(), set()
    for level, title in scan_headings(template):
        target = wildcards if is_wildcard(title) else literals
        target.add(level if is_wildcard(title) else (level, title))
    return literals, wildcards


def find_structural_noise(model_type: type, markdown: str, name: str = "") -> StructuralNoiseReport:
    """The document's headings that the model does not declare.

    Args:
        model_type: The `StructuredNLDoc` subclass the document is tracked as.
        markdown: The document's Markdown source.
        name: Document name, used only in the error message.

    Returns:
        A report; `report.clean` is True when every heading is declared.
    """
    template = getattr(model_type, "__template__", "") or ""
    literals, wildcards = declared_headings(template)
    undeclared = _undeclared(scan_headings(markdown), literals, wildcards)
    return StructuralNoiseReport(document=name, model=getattr(model_type, "__name__", "?"), undeclared=undeclared)


def _undeclared(headings: list[tuple[int, str]], literals: set, wildcards: set) -> list[str]:
    """Each heading line the template never accounts for, in document order."""
    from sldb.api.documents.heading_scan import format_heading

    missing = [(lv, ti) for lv, ti in headings if lv not in wildcards and (lv, ti) not in literals]
    return [format_heading(level, title) for level, title in missing]
