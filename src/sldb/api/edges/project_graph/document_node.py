"""A document of the project as a graph node."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.node_provenance import NodeProvenance


class DocumentNode(BaseModel):
    """One file of a document surface, named by its id, title slug or path."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(description="`kind:identity`, the id edges point at.")
    kind: str = Field(description="The surface kind of the document.")
    identity: str = Field(description="What names the document within its kind.")
    path: str = Field(description="Repo-relative POSIX path of the document.")
    label: str = Field(description="Title of the document, or one made from its file name.")
    provenance: NodeProvenance = Field(description="Where the node came from.")
    document_id: str | None = Field(default=None, description="The `id` the document declares, if any.")

    def to_dict(self) -> dict[str, Any]:
        """The node as plain data, every field included."""
        return self.model_dump()
