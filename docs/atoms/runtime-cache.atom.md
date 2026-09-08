# Runtime Cache

## Related Concepts

- [Store](store.atom.md)
- [Tracked Document](tracked-document.atom.md)
- [Address Space](address-space.atom.md)

## What It Is

The runtime cache is how sldb reads a store once per change instead of once per query, using the hash chain as the Merkle tree it is. `hash_a` says whether anything changed, a model's `hash_b` whether that model did, a document's `hash_c` whether that document did; a read descends only where a hash moved; the leaves are also stat-ed (no reads) so Markdown edited by hand is seen before `stores update` moves its hash, and `SLDB_TRUST_CHAIN=1` skips that sweep for a store only written through sldb. The yaml indexes are parsed once per file state and returned as copies; the extracted documents are kept whole-store (by `hash_a` and the `hash_b`s) and per document (by path, `hash_c` and model) in memory, mirrored in `.sldb/runtime/cache/extracted.json` so a new process skips extraction; each model's semantic contribution and sections are remembered by `hash_b` in `.sldb/runtime/cache/built.json` so a rebuild walks only models whose documents moved. A save that changes nothing leaves its file alone. Every write through sldb moves the chain from the leaf up, so the next read sees exactly what changed; the rebuilds keyed by `hash_b` see a hand edit once `stores update` rehashes it. Both cache files are derived: delete them freely and keep them out of git.

## Where It Lives

`sldb.store.runtime_cache` (memory), `sldb.store.runtime_cache_disk` (payload file), `sldb.store.built_cache` (per-model file), `sldb.store.io` (indexes), `sldb.store.semantic`, `sldb.store.semantic_doc_tags` and `sldb.store.section_rebuild` (rebuilds by `hash_b`), `sldb.cli.commands.store_update` (field hashes only for changed text), `sldb.store.migration` (no rewrite of a canonical layout).
