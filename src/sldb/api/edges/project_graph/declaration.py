"""One reference a document declares, before it is resolved."""

from __future__ import annotations

from typing import NamedTuple


class Declaration(NamedTuple):
    """A declared target, the role it is declared with, and where (`frontmatter`, `line:N:...`)."""

    target: str
    role: str
    locator: str
