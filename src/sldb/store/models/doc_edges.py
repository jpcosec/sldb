"""One document's shard of the edge index: `.sldb/runtime/edges/<Model>/<doc>.yaml`."""

from __future__ import annotations

from pydantic import Field

from sldb.store.models.edge_contribution import EdgeContribution


class DocEdges(EdgeContribution):
    """What a document contributes, stamped with the `hash_c` it was built from: a document
    whose `hash_c` still matches is never processed again."""

    doc_name: str = Field(description="Name of the contributing document within its model.")
    model_name: str = Field(default="", description="Model the contributing document is tracked under.")
    hash_c: str = Field(default="", description="The document's hash_c this shard was built from; the shard's cache key.")
    hash_d: str = Field(default="", description="The document's hash_d (its fields under the model's contract): it moves when the model changes even if the text, and so hash_c, does not.")
    semantic_tags: list[str] = Field(default_factory=list, description="The contributing document's tags, so a reader can leave out whole shards by tag (exclude_tags).")
