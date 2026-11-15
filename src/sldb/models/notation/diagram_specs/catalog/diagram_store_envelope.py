"""`diagram_store_envelope`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from sldb.models.notation.diagram_specs.catalog.diagram_store import DiagramStore


class DiagramStoreEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    diagram_store: DiagramStore
