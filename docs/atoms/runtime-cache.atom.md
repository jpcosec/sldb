# Runtime Cache

## Related Concepts

- [Store](store.atom.md)
- [Tracked Document](tracked-document.atom.md)
- [Address Space](address-space.atom.md)

## What It Is

The runtime cache is how sldb reads a store once per change instead of once per query, using the hash chain as the Merkle tree it is. `hash_a` says whether anything changed, a model's `hash_b` whether that model did, a document's `hash_c` whether that document did; a read descends only where a hash moved and never stats or reads documents to find out. The yaml indexes are parsed once per file state and returned as copies; the extracted documents are kept whole-store (by `hash_a` and the `hash_b`s) and per document (by path, `hash_c` and model) in memory, mirrored in `.sldb/runtime/cache/extracted.json` so a new process skips extraction; each model's semantic contribution and sections are remembered by `hash_b` in `.sldb/runtime/cache/built.json` so a rebuild walks only models whose documents moved. A save that changes nothing leaves its file alone. Every write through sldb moves the chain from the leaf up, so the next read sees exactly what changed; an edit made behind sldb's back waits for `stores update` to rehash it. Both cache files are derived: delete them freely and keep them out of git.

## Where It Lives

`sldb.store.runtime_cache` (memory), `sldb.store.runtime_cache_disk` (payload file), `sldb.store.built_cache` (per-model file), `sldb.store.io` (indexes), `sldb.store.semantic`, `sldb.store.semantic_doc_tags` and `sldb.store.section_rebuild` (rebuilds by `hash_b`), `sldb.cli.commands.store_update` (field hashes only for changed text), `sldb.store.migration` (no rewrite of a canonical layout).
