"""One document's shard of the edge index: `.sldb_cache/edges/<Model>/<doc>.yaml`."""

from __future__ import annotations

from pydantic import Field

from sldb.store.models.edge_contribution import EdgeContribution


class DocEdges(EdgeContribution):
    """What a document contributes, stamped with the `source_hash` it was built from: a document
    whose `source_hash` still matches is never processed again."""

    doc_name: str = Field(description="Name of the contributing document within its model.")
    model_name: str = Field(default="", description="Model the contributing document is tracked under.")
    source_hash: str = Field(default="", description="The document's source_hash this shard was built from; the shard's cache key.")
    content_hash: str = Field(default="", description="The document's content_hash (its fields under the model's contract): it moves when the model changes even if the text, and so source_hash, does not.")
    contract_hash: str = Field(default="", description="The model's contract_hash this shard was built under: a contract change (a new `__reference_models__`) moves the edges without moving the document's hashes.")
    semantic_tags: list[str] = Field(default_factory=list, description="The contributing document's tags, so a reader can leave out whole shards by tag (exclude_tags).")
    source_stat: list[int] | None = Field(default=None, description="`[mtime_ns, size]` (lstat) of the file whose text hashes to `source_hash`, taken when the shard was built: a read of the index whose file still has this stat does not open it. None on a shard built before it existed: that file is hashed as before, and the next build fills it in.")
