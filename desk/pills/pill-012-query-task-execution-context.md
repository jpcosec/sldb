---
id: pill-012-query-task-execution-context
tags:
- system:sldb
- topic:query
- topic:execution
---

# AST query task execution context

## What

_Define the context or guardrail this pill carries._

This task defines the first public query primitives that operate on SLDB document structure itself. It should describe what a user or downstream tool can ask about a document's structural units once addressability is defined.

## Why

_Explain why this context matters for safe execution._

SLDB already exposes store structural queries, but those queries are centered on tracked model/doc/field payload access. This task is about document-structure queries over AST-like units, not just store payload lookup.

## When

_Describe when an agent should apply this pill._

Apply this pill when designing document-local queries, selecting which structural units are queryable, or deciding what a stable query result shape should return.

## Where

_Name the files, surfaces, or scope this pill applies to._

Read these first:

- `desk/tasks/task-design-sldb-ast-query-primitives.md`
- `desk/pills/pill-011-addressability-task-execution-context.md`
- `src/sldb/cli/commands/query.py`
- `src/sldb/store/query_engine/structural.py`
- `src/sldb/store/query_engine/structural_queries.py`
- `src/sldb/core/ast.py`
- `docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`

Questions this pill covers:

- what unit types can be queried
- which queries require canonical addresses versus derived selectors
- what queries should return: text, metadata, structural nodes, or addresses
- which primitives belong in document-local APIs versus store-level CLI surfaces

## How

_Describe the correct way to apply this guidance._

Anchor the design in the addressability model. Show how each primitive consumes an address or selector and what stable result shape it returns.

Produce a durable design that names:

- the minimum query primitive set
- example inputs and outputs
- relation to existing `st` structural query surfaces
- follow-up implementation tasks if runtime work should be staged

## How Not

_Describe the shortcut or failure mode to avoid._

Do not silently overload current `st.{Model}.doc.field` semantics and call that AST query design if the result still cannot name or return meaningful document subunits.

