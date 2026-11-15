"""Create a document of a registered model."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from sldb.mcp.changes.base import _Change


class CreateDocument(_Change):
    """Create a document of a registered model."""

    action: Literal["create"]
    model: str = Field(description="A model the store registers.")
    name: str = Field(description="The new document's name, unique in the store.")
    payload: dict[str, Any] = Field(description="Every field of the document, as the model declares it.")
    path: str | None = Field(default=None, description="Markdown path relative to the project root; omitted, the model's default directory.")
