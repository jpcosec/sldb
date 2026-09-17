"""The edge index (fusion of kgdb's typed ingest into sldb): every node and typed edge of a
store, kept as per-document shards on the hash chain and composed on read.

- contributions (`doc_*`, `model_contribution`, `store_contribution`): what each shard holds;
- `compose` / `resolve` / `validation`: shards -> one `EdgeIndex`, cross-document rules applied
  and reported, never stored;
- `federation`: the linked stores' indexes, ids qualified with the store's name.
"""
