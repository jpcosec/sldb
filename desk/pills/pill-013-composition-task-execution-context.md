---
id: pill-013-composition-task-execution-context
tags:
- system:sldb
- topic:composition
- topic:execution
---

# Composition task execution context

## What

_Define the context or guardrail this pill carries._

This task expands SLDB composition beyond the two currently evidenced modes:

- document transclusion using `![[...]]` in `src/sldb/links.py`
- render-time child summarization using `StructuredNLDoc.__compositions__` in `src/sldb/models/structured_doc.py` and `tests/test_composition.py`

The task is to define what additional text-first composition modes belong in SLDB.

## Why

_Explain why this context matters for safe execution._

The repo already shows that SLDB can compose text both by document inclusion and by rendering summaries from referenced docs. The open question is how far that model should extend while remaining document-first and readable.

## When

_Describe when an agent should apply this pill._

Apply this pill when evaluating new composition modes, choosing what source units a composition can consume, or deciding how composed output should preserve provenance while staying readable.

## Where

_Name the files, surfaces, or scope this pill applies to._

Read these first:

- `desk/tasks/task-expand-sldb-composition-modes.md`
- `desk/pills/pill-011-addressability-task-execution-context.md`
- `desk/pills/pill-012-query-task-execution-context.md`
- `src/sldb/links.py`
- `src/sldb/models/structured_doc.py`
- `tests/test_composition.py`
- `docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`

Candidate composition modes to evaluate:

- section-level composition
- field-summary composition
- query-driven fragment composition
- multi-document sectional synthesis that still materializes readable text

## How

_Describe the correct way to apply this guidance._

Keep composition text-first. A useful test is whether the output can still be read as a coherent authored document artifact rather than merely as an intermediate graph projection.

Produce a design that states:

- the supported composition mode taxonomy
- what each mode consumes as input
- how each mode materializes text
- how provenance of composed fragments should be represented
- what code surfaces would likely host future implementation

## How Not

_Describe the shortcut or failure mode to avoid._

Do not define composition in a way that requires KGDB-style traversal or hidden graph semantics just to decide what text should appear.

