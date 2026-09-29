---
id: issue-sldb-stable-section-ids
status: open
tags:
- system:sldb
- topic:addressability
- topic:sections
- topic:feature
related_tasks:
- desk/tasks/task-correct-ast-ownership-and-section-contracts.md
- desk/tasks/task-define-sldb-addressability-model.md
---

# SLDB: sections have no stable id, so moving one changes its address

## Problem

Sections are addressed by hierarchical slug. Repeated headings are disambiguated by order of appearance. Two consequences (`docs/user-manual.md` §14):

- **Moving a section changes its address.** Nothing that held the old address survives the move.
- **Inserting a section before a same-named sibling silently re-points the old address** at different content, because disambiguation is positional.

The second is worse than a broken link: the address still resolves, just to the wrong section.

## Why this is a feature gap, not a bug

Slug addressing works as designed and is documented. What is missing is an identity layer: sections are the one addressable unit in SLDB with no identity independent of its position.

## Relationship to tracked tasks

This gap is **already named as the reason a task stays open**. `task-correct-ast-ownership-and-section-contracts` (status `open`) ends with:

> "Stable addressing for repeated sibling headings remains a design gap; keep this task open until it is decided and the delivery audit is complete."

So this is not new work — it is the explicit blocker on an open task. `docs/addressability_model.md` already states the contract side: "Section paths break when a heading changes. Treat them as navigational, not as long-lived links."

Decide before starting: fold this into that task, or make the task depend on this issue. Do not run them as parallel efforts.

`task-define-sldb-addressability-model` (`current_node: completed`) produced the model that documents the limit; it is the contract this change would amend.

## What's needed

- A stable per-section id that survives retitling and reordering.
- Slug addressing kept as the human-facing form; the stable id is what references persist.
- A documented resolution order when both are available, and a real error when they disagree.

## Files to read first

- `src/sldb/store/models/doc_sections.py` — the `DocSections` shape; the comment at line 11 already names the identity rule (unique slugs, spans)
- `src/sldb/store/section_doc_contribution.py` — where a document's sections shard is built and cached
- `src/sldb/store/section_rebuild.py` — the parse that assigns slugs
- `src/sldb/store/section_sync.py` — when shards are considered current
- `docs/addressability_model.md` — the addressing contract this has to fit inside

## Design considerations

- **Where does the id come from?** A content hash moves when the section is edited, which defeats the purpose. A positional index is what we already have. This likely needs an id minted on first sight and persisted in the shard.
- **Persistence**: minted ids must survive a `runtime/` wipe, but `runtime/` is documented as disposable cache (§4). That argues for `core/`, which makes section identity versioned state — a real scope decision, not an implementation detail.
- **Rename vs delete+create**: a moved section and a deleted-plus-new section are indistinguishable from content alone. Decide whether to attempt matching or accept the ambiguity.
- **Blast radius**: composition and the semantic index both consume section addresses. This is not a local change.

## Task list

- [ ] **First**: reconcile with `task-correct-ast-ownership-and-section-contracts` — fold in, or declare a dependency
- [ ] Write down the identity contract: what a section id promises across edit, move, retitle, delete
- [ ] Decide `core/` vs `runtime/` persistence and record the reasoning
- [ ] Decide rename-detection policy (attempt matching, or treat as delete+create)
- [ ] Implement id minting and persistence in the sections shard
- [ ] Support both addressing forms with a documented resolution order
- [ ] Tests: move, retitle, insert-before-same-named-sibling, delete, `runtime/` wipe and rebuild
- [ ] Update `docs/addressability_model.md` and `docs/user-manual.md` §14

## Pills

- `desk/pills/pill-011-addressability-task-execution-context.md` — execution context for addressability work
- `desk/pills/pill-005-store-health-is-sldb-owned.md` — the `core/` vs `runtime/` placement decision is a store-health question
