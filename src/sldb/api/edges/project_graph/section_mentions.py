"""Mentions read under chosen Markdown headings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.mention_pattern import MentionPattern


class SectionMentions(BaseModel):
    """Patterns read on the lines below a heading (level 2 to 6) named in `headings`."""

    model_config = ConfigDict(frozen=True)

    headings: tuple[str, ...] = Field(description="Lower-cased, space-collapsed heading texts whose lines are read.")
    patterns: tuple[MentionPattern, ...] = Field(description="Patterns applied to each line, in order.")
    role: str = Field(description="Edge role of every mention.")
    kinds: tuple[str, ...] = Field(default=(), description="Node kinds read; empty reads every document.")
