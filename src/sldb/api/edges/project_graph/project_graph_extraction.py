"""Every declared edge and missing target of a project."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.missing_project_target import MissingProjectTarget
from sldb.api.edges.project_graph.project_edge import ProjectEdge


class ProjectGraphExtraction(BaseModel):
    """The whole project graph's edges and findings, each sorted by its key."""

    model_config = ConfigDict(frozen=True)

    edges: list[ProjectEdge] = Field(description="Declared edges whose target exists.")
    missing_targets: list[MissingProjectTarget] = Field(description="Declared targets that resolve to no node.")
