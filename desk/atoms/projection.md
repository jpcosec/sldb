---
layer: core
id: projection
title: Projection
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-projections
provenance: source docs/core/reasoning.md
---

# Projection

## Answer

A projection is a deterministic derived view computed from canonical kernel/database state under an explicit projection specification and engine version.

## Supporting points

- A projection selects, reorganizes, or interprets canonical state for a specific purpose.
- Semantic graphs, backlinks, dependency views, anchor maps, and other specialized graph/runtime views are projections.
- Generic renders or materializations such as Markdown, HTML, JSON, or API payloads should be described as renders/materializations rather than as projections unless a doc needs both terms explicitly.
- Projections never become the primary authority for the document; they are cached or persisted as derived artifacts.
- A projection result must remain traceable to `revision + projection spec + engine version + source hash`.
- Projection invalidation is allowed and expected; rebuildability is a core property of the architecture.

## Related atoms

### Depends on

- [depends_on:: [[projection-spec]]]
- [depends_on:: [[revision]]]
- [depends_on:: [[graph-store]]]

### Supports

- [supports:: [[projection-surface]]]
- [supports:: [[document-materializer]]]
- [supports:: [[semantic-exporter]]]
- [supports:: [[search-projection]]]
- [supports:: [[embeddings]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
