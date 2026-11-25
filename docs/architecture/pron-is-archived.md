# ADR: pron Is Archived

- Status: Accepted, not yet executed in code
- Date: 2026-11-25
- Decision Maker: the owner
- Supersedes: the section "pron is a semantic shell" of [SLDB Absorbs KGDB](sldb-absorbs-kgdb.md)
  (2026-09-20)
- Related repos: `pron`, `sldb`, `graph_ui`, `legos`

## Context

The 2026-09-20 ADR shrank pron to a semantic shell: it dropped its store facade, its graph reader
and its corpus, and kept saying and evaluating forms, and moves with their ledger and undo. It also
said that graph_ui is a UI over SLDB, not a surface over pron.

Two months later:

- graph_ui still opens the store through `pron.world.store.Store` in its default local mode. Every
  call it makes has an equivalent in `sldb.api`.
- pron's suite is red against current SLDB, with a task blocked since 2026-11-16.
- specIR was decided not to depend on pron (2026-11-11).
- No project in the workspace uses pron's language layer. `legos`, outside the workspace, does.
- The owner believed pron was already retired. No record said so, which is how the question
  resurfaced.

## Decision

pron is archived: no new work, the code stays as reference. The door to a store is the SLDB API,
for interfaces and for agents.

What moves to SLDB, because editing from an interface needs it:

1. Rejecting a relation before it is written, by its types, cardinality and condition. SLDB
   detects it afterwards today (`check_edges`).
2. Prevalidating a whole move, with its conditions and transitions.
3. A persistent ledger of moves, and undo across sessions. SLDB's MCP undo is per session and in
   memory.

What does not move: session projections (what a session may name), forms, lexicon, dialogue, the
language surface and the `goal` planner. Simulating the effect of editing a rule moves only if it
is asked for.

## Consequences

- graph_ui's adapter (`sldb_adapter.py`) stops importing pron. Gesture editing in graph_ui writes
  through SLDB; the September design that wrote pron forms through a `GestureDoc` is void.
- The gate `G_SLDB_PRON_MCP` in specIR's plan is replaced by the three capabilities above.
- `legos` loses read-only sessions by projection. The owner accepted it: legos is a separate repo
  and will be migrated to Kimun when it is resumed.
- pron's README carries the archive notice (`53165c6`). Its registry entry and its GitHub
  repository are not yet marked.

## Not verified

- Whether `kinesis` uses pron; Kimun's README says so.
