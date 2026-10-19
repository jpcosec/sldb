---
id: issue-sldb-one-way-composition-no-edit-through
status: open
tags:
- system:sldb
- topic:composition
- topic:feature
related_tasks:
- docs/composition_modes.md
---

# SLDB: composition is one-way — no edit-through, no composition by query

## Problem

Composition resolves references and assembles a composed view, but the path is read-only (`docs/user-manual.md` §14):

- **No edit-through.** Editing a composed view does not propagate to the source documents. To change composed content you locate the source and edit it there.
- **No composition by query.** Composition targets are named explicitly; a composed document cannot be defined as "every doc matching this query".

The combination means a composed view is a rendering, not a working surface.

## Why this is a feature gap, not a bug

One-way composition is the documented contract and it does what it claims. What is absent is write direction and dynamic membership.

## Relationship to tracked tasks

**This overlaps `task-expand-sldb-composition-modes` (closed in 76546236; its design is in `docs/composition_modes.md`) almost exactly.** That task's scope read:

> "Consider transclusion composition, summary composition, sectional composition, and query-driven semantic composition while preserving authored locality and readable textual outputs."

It is `status: active` with `current_node: completed`. But `docs/composition_modes.md:42` says the opposite of delivery:

> "Section-only transclusion, query-driven composition, and edits propagated from composed output to source documents **were proposals. They are not advertised as supported operations in this checkout.**"

A task sits at `completed` while the doc it produced says the work was not done. Resolve that first: either it was a *design* task whose deliverable was a documented gap, or the status is wrong. Starting here before settling it means doing the work twice.

`docs/composition_modes.md:25` independently confirms the edit-through half: "There is no implemented edit-through operation from a summary to its child document."

## What's needed

Two separable pieces, worth treating as separate slices:

1. **Edit-through** — a write against a composed address routes to the owning source document.
2. **Composition by query** — membership defined by a query, resolved at composition time.

## Files to read first

- `docs/composition_modes.md` — the current composition contract
- `src/sldb/cli/commands/` — the `compose` command surface
- `src/sldb/api/` — composition entry points and what they return
- `docs/addressability_model.md` — how a composed address maps back to a source address
- `src/sldb/cli/commands/find*.py` — the existing query surface, if membership is to reuse it

## Design considerations

- **Ownership is the hard part of edit-through.** A composed region must map unambiguously to exactly one source field. Where composition transforms or merges content, that map may not exist — those regions have to be explicitly read-only rather than silently dropping writes.
- **Conflict detection**: the store already returns a real 409 on a mismatched `expected` over HTTP (§16). Edit-through should reuse that, not invent a second concurrency story.
- **Query-defined membership is unstable by construction.** The composed document changes when unrelated documents are created. Decide whether membership is resolved on read or pinned at compose time.
- **Hash implications**: a composed document whose membership comes from a query has no stable `source_hash` input. That interacts directly with the store's Merkle model (§4).
- **Anti-pattern guard**: the manual's §15 says not to reimplement composition or reference resolution elsewhere. The lack of edit-through is exactly what tempts a consumer to do it.

## Task list

- [x] **First**: resolve whether `task-expand-sldb-composition-modes` at `completed` was design-only or mis-statused — it was a design task, closed in 76546236; this issue is its execution half
- [ ] Split into two slices: edit-through, and query-defined membership
- [ ] Specify the composed-address → source-field ownership map, including regions that cannot have one
- [ ] Mark non-mappable composed regions read-only and error on writes to them
- [ ] Implement edit-through reusing the existing `expected` / 409 concurrency contract
- [ ] Decide read-time vs compose-time membership resolution for queries, and settle the hashing consequence
- [ ] Tests: write-through to a single owner, rejected write to a merged region, stale `expected` yields 409, membership change on new matching document
- [ ] Update `docs/composition_modes.md` and `docs/user-manual.md` §14

## Pills

- `docs/composition_modes.md` — the composition design (pill-013, its execution context, was retired on 2026-10-18)
- `docs/addressability_model.md` — edit-through is an addressability problem before it is a write problem
