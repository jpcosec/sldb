---
id: pill-010-active-board-slice-execution-map
tags:
- system:sldb
- workspace:desk
- topic:execution
- topic:design
---

# Active board slice execution map

## What

_Define the context or guardrail this pill carries._

This board is a four-task design slice for SLDB document structure. The slice defines the contracts that later implementation work will consume:

1. addressability of meaningful textual units;
2. structural query primitives over those units;
3. richer text-first composition modes;
4. provenance-preserving semantic export to downstream graph systems.

A zero-context agent should treat these tasks as one ordered design chain, not as independent tickets.

## Why

_Explain why this context matters for safe execution._

The current repo already has partial surfaces for AST parsing, store structural querying, transclusion, render-time composition, and semantic export. Those surfaces encode assumptions, but the cross-cutting contract connecting them is still under-specified. This board exists to make those assumptions explicit before broad runtime expansion.

## When

_Describe when an agent should apply this pill._

Apply this pill when working on the active board slice around addressability, query, composition, and semantic export design, especially when a change could harden assumptions before the upstream contract is written down.

## Where

_Name the files, surfaces, or scope this pill applies to._

Read these before changing anything in this slice:

- `desk/tasks/Board.md`
- `desk/tasks/task-define-sldb-addressability-model.md`
- `desk/tasks/task-design-sldb-ast-query-primitives.md`
- `desk/tasks/task-expand-sldb-composition-modes.md`
- `desk/tasks/task-tighten-semantic-export-provenance-contract.md`
- `docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`
- `docs/architecture/semantic-export-boundary.md`
- `src/sldb/core/ast.py`
- `src/sldb/models/structured_doc.py`
- `src/sldb/links.py`
- `src/sldb/cli/commands/query.py`
- `src/sldb/store/query_engine/structural.py`
- `src/sldb/store/query_engine/structural_queries.py`
- `src/sldb/store/export.py`
- `tests/test_composition.py`

## How

_Describe the correct way to apply this guidance._

Work text-first and contract-first. Use existing repo surfaces as evidence, describe what is already true, then define the missing contract in a way later tasks can consume without reopening the architecture debate.

Use this execution order unless the board changes explicitly:

1. `task-define-sldb-addressability-model`
2. `task-design-sldb-ast-query-primitives`
3. `task-expand-sldb-composition-modes`
4. `task-tighten-semantic-export-provenance-contract`

This slice should primarily produce durable design artifacts:

- architecture docs or ADR-style docs under `docs/architecture/`
- atoms if a concept becomes reusable beyond a single task
- follow-up implementation tasks if runtime changes are implied but not yet safe to harden
- code changes only when needed to validate or demonstrate a now-explicit contract

## How Not

_Describe the shortcut or failure mode to avoid._

Do not start by scattering code changes across query, composition, and export surfaces without first documenting the contract those changes are supposed to implement.

