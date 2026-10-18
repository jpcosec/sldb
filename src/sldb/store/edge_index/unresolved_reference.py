"""A declared reference the composed index could not point at a node."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class UnresolvedReference(BaseModel):
    """One value of a declared reference or containment field that resolves to no document.

    A normal condition a caller inspects, kept apart from `EdgeIndex.problems` (which fails
    authored edges). Only fields the model declared appear: a free `__references__` field
    reports its unqualified values only when they look like a path.
    """

    source: str = Field(description="Export id of the document holding the reference, e.g. `TaskDoc:task-a`.")
    model: str = Field(description="Model of the source document.")
    field: str = Field(description="The declared field holding the value.")
    target: str = Field(description="The value as written: a bare id, an export id or a path.")
    target_export_id: str | None = Field(default=None, description="The export id the value names, when it can be qualified (only the document is missing).")
    relation: Literal["references", "contains"] = Field(description="`contains` for a `__containment__` field, `references` otherwise.")
    reason: Literal["missing_document", "ambiguous", "unknown_path"] = Field(description="No such document; several allowed models have one; a path no tracked document has.")
    source_path: str | None = Field(default=None, description="Project-relative path of the source document (its own store's root for a linked one).")
