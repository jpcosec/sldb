---
id: atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
title: The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git
  history is the past
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-layout
- topic:journal
---

# The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git history is the past

## Answer

An sldb store is two sibling directories at the repo root: .sldb/ holds store.yaml and core/ (store_index, models, documents) and is versioned in git; .sldb_cache/ holds everything derived (edges, sections, semantic, graphs, caches, locks), is git-ignored and is rebuilt by stores build. There is no journal: the past of a store is asked of git history (sldb docs history). stores check fails with stores/core_ignored when core/ or store.yaml are ignored and alerts with stores/cache_not_ignored when the cache line is missing; stores migrate-layout moves an old .sldb/runtime/ into .sldb_cache/. Owner decision of 2026-10-29.
