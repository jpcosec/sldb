# Runtime Cache

## Related Concepts

- [Store](store.atom.md)
- [Tracked Document](tracked-document.atom.md)
- [Address Space](address-space.atom.md)

## What It Is

The runtime cache is how sldb reads a store once per change instead of once per query. The yaml indexes are parsed once and returned as copies; the extracted documents are kept whole-store and per document in memory, validated by the path, mtime and size of every file a load depends on; and the extracted payloads are mirrored in `.sldb/runtime/cache/extracted.json` so a new process skips extraction for documents it has already seen. A save that changes nothing leaves its file alone, and the semantic and sections rebuilds remember each document's result by the same signature. Every write through sldb touches an index or a document, so the next read sees a new signature and reloads only what changed. The cache file is derived: delete it freely and keep it out of git.

## Where It Lives

`sldb.store.runtime_cache` (memory), `sldb.store.runtime_cache_disk` (the file), `sldb.store.io` (indexes), `sldb.store.semantic` and `sldb.store.section_rebuild` (per-document rebuild results), `sldb.cli.commands.store_update` (field hashes only for changed text), `sldb.store.migration` (no rewrite of a canonical layout).
