"""One model's shard of the edge index: `.sldb_cache/edges/<Model>.yaml`."""

from __future__ import annotations

from pydantic import Field

from sldb.store.models.edge_contribution import EdgeContribution


class ModelEdges(EdgeContribution):
    """What a registered model contributes: its node, its field nodes, `has_field`, `extends`."""

    model_name: str = Field(description="Name of the contributing model.")
    projected_fields: list[str] = Field(default_factory=list, description="Fields a payload filter may name for this model's documents: its `__indexed__`, else every field whose type can hold a scalar or a list of scalars. Empty when the model could not be loaded.")
