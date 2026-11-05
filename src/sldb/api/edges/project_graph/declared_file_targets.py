"""Documents whose frontmatter names a project file that must be a graph node."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DeclaredFileTargets(BaseModel):
    """A frontmatter field, in a glob of documents, whose value is a repo-relative file path.

    A declared file that exists inside the project, is no document and no rule already
    classified becomes a node, so references to it resolve.
    """

    model_config = ConfigDict(frozen=True)

    directory: str = Field(description="Directory of the declaring documents, relative to the project root.")
    pattern: str = Field(default="*.md", description="Recursive glob of the declaring documents below `directory`.")
    field: str = Field(description="Top-level frontmatter field holding the declared path.")
    kind: str = Field(description="Node kind of the declared file.")
    file_kind: str = Field(description="What the declared file is to the project.")
    source_kind: str = Field(description="Provenance `source_kind` of the node, naming why it exists.")
