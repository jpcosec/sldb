"""A project file (source, test, config, spec) as a graph node."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.node_provenance import NodeProvenance


class FileNode(BaseModel):
    """One file a path rule or a declaration made a node, named by its path."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(description="`kind:path`, the id edges point at.")
    kind: str = Field(description="Node kind given by the rule.")
    identity: str = Field(description="The repo-relative path.")
    path: str = Field(description="Repo-relative POSIX path of the file.")
    file_kind: str = Field(description="What the file is to the project.")
    provenance: NodeProvenance = Field(description="Where the node came from.")

    def to_dict(self) -> dict[str, Any]:
        """The node as plain data."""
        return self.model_dump()
