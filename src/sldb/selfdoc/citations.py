"""Docstring citations a consumer can build `implements` edges from: the `spec NN`
references a module or command docstring cites, read back in order.
"""

from __future__ import annotations

import re

SPEC_REF = re.compile(r"\bspec\s+(\d{2}[a-z]?)\b", re.I)


def cites(docstring: str | None) -> list[str]:
    """The distinct chapter numbers a docstring cites (`spec 06`, `spec 11 §2`), sorted."""
    return sorted(set(SPEC_REF.findall(docstring or "")))
