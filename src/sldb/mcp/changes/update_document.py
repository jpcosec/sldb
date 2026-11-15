"""Set fields of a tracked document."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from sldb.mcp.changes.base import _Change


class UpdateDocument(_Change):
    """Set fields of a tracked document; the rest of its payload stays as it is."""

    action: Literal["update"]
    model: str
    name: str
    fields: dict[str, Any] = Field(description="Dotted field path -> new value (sldb.api.deep_set).")
