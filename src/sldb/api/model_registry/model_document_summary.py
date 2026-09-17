"""One tracked document of a registered model, as `describe_model` lists it."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ModelDocumentSummary(BaseModel):
    """Where a tracked document lives and how it is tagged."""

    name: str = Field(description="Document name, unique within its model.")
    path: str = Field(description="Markdown path as recorded in the documents index.")
    semantic_tags: list[str] = Field(description="Semantic tags the document carries in the store index.")
