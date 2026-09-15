"""---
id: sldb.selfdoc.planned_document
kind: core
tags: [system:sldb, workspace:knowledge, topic:selfdoc]

---
Declare the planned-document contract shared by planning, persistence, and
inspection.

This module defines the record materializers hand to the write and inspect
workflows. It does not write files, register models, or decide which
documents need saving.
"""
from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel, Field
from sldb.models.knowledge_surface import CliCommandDoc, PythonSymbolDoc, SurfaceDoc


class PlannedDocument(BaseModel):
    """---
    id: sldb.selfdoc.planned_document.PlannedDocument
    kind: core
    tags: [type:code.symbol]

    ---
    Carry one validated documentation change and its before-image to execution.

    Materializers fill ``payload`` and ``markdown`` after a render/extract
    roundtrip check; ``write_documents`` persists them through SLDB tracking
    and ``inspect_documents`` reads them without writing. It is a planning
    record, not a filesystem transaction: ``previous`` is the before-image
    captured at planning time and ``changed`` flags parser-owned drift, while
    the write path re-verifies the file before saving.
    """

    path: Path = Field(description="Resolved destination Markdown file.")
    payload: CliCommandDoc | PythonSymbolDoc | SurfaceDoc = Field(description="Validated expected payload.")
    markdown: str = Field(description="Rendered, roundtrip-checked text.")
    previous: str | None = Field(description="Original text; None means missing file.")
    changed: bool = Field(description="Whether parser-owned fields need updating.")

    @property
    def model_name(self) -> str:
        """Registered model that owns this document."""
        return type(self.payload).__name__
