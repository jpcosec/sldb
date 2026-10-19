---
id: issue-sldb-sections-have-no-own-hash
status: open
tags:
- system:sldb
- topic:sections
- topic:performance
- topic:feature
related_tasks:
- desk/issues/issue-sldb-stable-section-ids.md
related_issues:
- desk/issues/issue-sldb-stable-section-ids.md
---

# SLDB: sections have no hash of their own, so any document edit reprocesses all of them

## Problem

`DocSections` is stamped with the parent document's `source_hash`. That hash is a cache key, not a level in the Merkle tree (`docs/user-manual.md` §14). Confirmed in `src/sldb/store/section_doc_contribution.py:21`: a shard is reused only when `cached.source_hash == doc.source_hash`.

So editing one section reprocesses every section of the document. There is no way to ask whether an individual section changed.

## Why this is a feature gap, not a bug

The cache is correct — it never serves stale sections. It is simply coarser than the data allows, and it leaves sections outside the hash model that covers the rest of the store.

## Relationship to tracked work

Gated by `issue-sldb-stable-section-ids`, which owns the stable-addressing gap since `task-correct-ast-ownership-and-section-contracts` closed on 2026-10-18. The chain is:

```
issue-sldb-stable-section-ids (open)
  └─ gates: per-section hashes (this issue)
```

That task's validation list already includes "Assert the same section schema before and after index rebuild" — adding a per-section hash changes that schema, so this cannot land without it.

## What's needed

- A per-section content hash stored in the shard.
- Reuse of unchanged sections when the parent document's hash moves.
- Sections positioned as a real level of the Merkle tree rather than a flat cache keyed by the parent.

## Files to read first

- `src/sldb/store/models/doc_sections.py` — the shard shape; lines 8-11 spell out that `source_hash` is the parent's and that the identity rule can force a re-parse anyway
- `src/sldb/store/section_doc_contribution.py:21` — the exact reuse condition to refine
- `src/sldb/store/section_rebuild.py` — the parse that would produce per-section hashes
- `src/sldb/store/section_sync.py:46` — the note about confirming agreement with an unmoved `source_hash`
- `docs/user-manual.md` §4 — the four-hash model this has to fit into

## Design considerations

- **Parsing is not the expensive part to skip.** Identifying which sections changed still requires parsing the document. The saving is downstream: semantic re-embedding and edge work per section. Scope the win honestly.
- **Interaction with the identity rule.** The shard already re-parses on unique-slug and span changes even when `source_hash` holds. Per-section hashes do not remove that; they have to compose with it.
- **This is entangled with stable section ids.** A per-section hash without a stable id cannot answer "did *this* section change" across a move — only "does a section with this content exist". See `issue-sldb-stable-section-ids`.
- **Merkle placement**: adding a level changes what `store_hash` composes from. Changing the existing hash composition would invalidate every existing store, which §4 explicitly rules out.
- Pairs directly with the per-field embedding index (`issue-sldb-embedding-index-not-field-granular`): both exist to avoid recomputing unchanged content.

## Task list

- [ ] **Blocked**: sequence after `issue-sldb-stable-section-ids`; per-section hashes need stable identity to be useful
- [ ] Confirm the schema change keeps the rebuild-parity check green (`tests/store/test_section_rebuild.py`)
- [ ] Measure what a per-section hash actually saves (embedding and edge work, not parsing)
- [ ] Add a per-section content hash to the sections shard
- [ ] Refine the reuse condition in `section_doc_contribution.py` to per-section granularity
- [ ] Compose with the existing identity rule instead of bypassing it
- [ ] Decide the Merkle placement without invalidating existing stores
- [ ] Tests: edit one section reuses the others, moved section, split/merged section, full rebuild parity
- [ ] Update `docs/user-manual.md` §4 and §14

## Pills

- `desk/contexts/pill-store-health-is-owned-by-sldb.md` — the hash model and rebuild cost are SLDB's own
- `docs/addressability_model.md` — section identity gates this work (pill-011 was retired on 2026-10-18)
