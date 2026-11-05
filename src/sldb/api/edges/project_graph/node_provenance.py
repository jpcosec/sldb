"""Where a project graph node came from."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class NodeProvenance(BaseModel):
    """The file a node stands for and the rule that made it a node."""

    model_config = ConfigDict(frozen=True)

    path: str = Field(description="Repo-relative POSIX path of the node's file.")
    source_kind: str = Field(description="Why the file is a node: `file_metadata`, `path_rule`, or a declaration.")
    extractor: str = Field(description="Name and version of the reader that made the node.")
