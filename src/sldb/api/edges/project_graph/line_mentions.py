"""Mentions read on every line of a document."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.mention_pattern import MentionPattern


class LineMentions(BaseModel):
    """Patterns read on each line of the documents of some kinds (paths a task names)."""

    model_config = ConfigDict(frozen=True)

    kinds: tuple[str, ...] = Field(description="Node kinds read.")
    excluded_path_prefixes: tuple[str, ...] = Field(default=(), description="Document paths below these trees are not read.")
    skipped_frontmatter_fields: tuple[str, ...] = Field(default=(), description="Frontmatter lines of these fields are not read.")
    patterns: tuple[MentionPattern, ...] = Field(description="Patterns applied to each line, in order.")
    role: str = Field(description="Edge role of every mention.")
    locator: str = Field(description="Locator label: a mention on line N is located at `line:N:<label>`.")
