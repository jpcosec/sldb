"""---
id: sldb.selfdoc.report
kind: core
tags: [system:sldb, workspace:knowledge, topic:selfdoc]

---
Declare the freshness-findings contract shared by selfdoc check and sync.

This module defines the typed report that inspection fills and the CLI prints
as JSON. It does not scan source, write documents, or resolve drift.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentationReport(BaseModel):
    """---
    id: sldb.selfdoc.report.DocumentationReport
    kind: core
    tags: [type:code.symbol]

    ---
    Report drift between parser-derived plans, files, and store tracking.

    ``inspect_documents`` fills the findings and the CLI prints them as JSON, with
    each one as an error or an alert (``sldb.selfdoc.report_findings``). ``ok``
    controls the exit status of check, sync and their Python variants: it is false
    only on an error (malformed metadata, a source graph missing or unreadable).
    Stale or ungenerated documents, stale hashes and rename hints are alerts: the
    source moved, the command exits 0, and the JSON lists them under ``alerts``.
    Removed documents are retained; rename candidates are heuristic hints without a
    uniqueness guarantee. ``ok`` ignores ``semantic_gaps``, which counts authored
    placeholders, and does not establish semantic completeness or docstring quality.
    """

    documents: int = Field(default=0, description="Expected command and surface documents.")
    missing: list[str] = Field(default_factory=list, description="Documents not yet materialized.")
    changed: list[str] = Field(default_factory=list, description="Documents with stale parser fields.")
    untracked: list[str] = Field(default_factory=list, description="Documents missing from the store.")
    stale_indexes: list[str] = Field(default_factory=list, description="Document hashes need refresh.")
    removed: list[str] = Field(default_factory=list, description="Retained documents absent from the parser.")
    renamed: list[dict[str, str]] = Field(default_factory=list, description="Unverified rename hints without a uniqueness guarantee.")
    semantic_gaps: int = Field(default=0, description="Symbols whose authored purpose or architecture remains undeclared.")
    graph_stale: list[str] = Field(default_factory=list, description="Source graphs stale against the scanned AST.")
    graph_errors: list[str] = Field(default_factory=list, description="Source graphs missing or unreadable, as path (state).")
    undeclared: int = Field(default=0, description="Declarations (modules, classes, functions) whose docstring declares no metadata.")
    unexplained: list[str] = Field(default_factory=list, description="Declarations with metadata but no explanation in their docstring, as path:line.")
    unresolved_references: list[str] = Field(default_factory=list, description="Annotation references no import or definition resolves, as path:line: name.")
    purpose_conflicts: list[str] = Field(default_factory=list, description="Symbol documents whose authored purpose differs from their docstring's first paragraph; kept until reconciled by hand.")
    metadata_errors: list[str] = Field(default_factory=list, description="Malformed docstring metadata and duplicate declared ids, as path:line: problem; python-sync writes nothing while any remain.")
    written: int = Field(default=0, description="Markdown documents written by sync.")

    @property
    def ok(self) -> bool:
        """Whether no error was found; alerts (stale documents, hashes, graph) do not count."""
        return not (self.metadata_errors or self.graph_errors)
