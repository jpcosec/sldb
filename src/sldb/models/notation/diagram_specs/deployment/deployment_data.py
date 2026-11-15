"""`deployment_data`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.deployment.artifact_model import ArtifactModel
from sldb.models.notation.diagram_specs.deployment.connection_model import ConnectionModel
from sldb.models.notation.diagram_specs.deployment.deployment_node_model import DeploymentNodeModel


class DeploymentData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nodes: dict[str, DeploymentNodeModel] = Field(
        description="Deployment nodes keyed by identifier."
    )
    artifacts: dict[str, ArtifactModel] = Field(
        default_factory=dict, description="Deployable artifacts keyed by identifier."
    )
    connections: list[ConnectionModel] = Field(
        default_factory=list,
        description="Communication paths between nodes (or artifacts) and «deploy»/«manifest» relations from artifacts.",
    )
