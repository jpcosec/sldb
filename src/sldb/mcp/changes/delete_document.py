"""Delete a tracked document."""

from __future__ import annotations

from typing import Literal

from sldb.mcp.changes.base import _Change


class DeleteDocument(_Change):
    """Delete a tracked document and its file."""

    action: Literal["delete"]
    model: str
    name: str
