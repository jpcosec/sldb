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

    ``inspect_documents`` fills the findings and the CLI prints them as JSON;
    ``ok`` controls CLI check/sync exit status, but the Python variants currently
    return zero even when the JSON reports false. Removed documents are retained;
    rename candidates are heuristic hints without a uniqueness guarantee.
    ``ok`` means none of the checked freshness findings were populated. It ignores
    ``semantic_gaps``, which counts authored placeholders, and does not establish
    semantic completeness, docstring quality, or complete removal detection.
    """

    documents: int = Field(default=0, description="Expected command and surface documents.")
    missing: list[str] = Field(default_factory=list, description="Documents not yet materialized.")
    changed: list[str] = Field(default_factory=list, description="Documents with stale parser fields.")
    untracked: list[str] = Field(default_factory=list, description="Documents missing from the store.")
    stale_indexes: list[str] = Field(default_factory=list, description="Document hashes need refresh.")
    removed: list[str] = Field(default_factory=list, description="Retained documents absent from the parser.")
    renamed: list[dict[str, str]] = Field(default_factory=list, description="Unverified rename hints without a uniqueness guarantee.")
    semantic_gaps: int = Field(default=0, description="Symbols whose authored purpose or architecture remains undeclared.")
    kgdb_stale: list[str] = Field(default_factory=list, description="KGDB source graphs missing or stale against the scanned AST.")
    written: int = Field(default=0, description="Markdown documents written by sync.")

    @property
    def ok(self) -> bool:
        """Whether all expected records and indexes are current."""
        return not any((self.missing, self.changed, self.untracked, self.stale_indexes, self.removed, self.renamed, self.kgdb_stale))
