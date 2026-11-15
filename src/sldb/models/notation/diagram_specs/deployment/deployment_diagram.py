"""`deployment_diagram`."""

from __future__ import annotations

from typing import Literal
from pydantic import Field

from sldb.models.notation.diagram_specs.base.base_diagram import BaseDiagram
from sldb.models.notation.diagram_specs.deployment.deployment_data import DeploymentData
from sldb.notations.diagram_type import DiagramType


class DeploymentDiagram(BaseDiagram):
    type: Literal[DiagramType.deployment] = Field(
        default=DiagramType.deployment,
        description="Discriminator for deployment diagram specs.",
    )
    data: DeploymentData = Field(
        description="Deployment-specific nodes, artifacts, and connections."
    )
