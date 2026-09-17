"""One model's shard of the edge index: `.sldb/runtime/edges/<Model>.yaml`."""

from __future__ import annotations

from pydantic import Field

from sldb.store.models.edge_contribution import EdgeContribution


class ModelEdges(EdgeContribution):
    """What a registered model contributes: its node, its field nodes, `has_field`, `extends`."""

    model_name: str = Field(description="Name of the contributing model.")
