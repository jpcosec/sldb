"""`DiagramType`: los tipos de diagrama que una notacion puede dibujar."""

from __future__ import annotations

from enum import Enum


class DiagramType(str, Enum):
    class_ = "class"
    component = "component"
    sequence = "sequence"
    state = "state"
    activity = "activity"
    deployment = "deployment"
    component_view_matrix = "component_view_matrix"
    reflection = "reflection"
