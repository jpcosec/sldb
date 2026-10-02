---
id: pill-014-semantic-export-task-execution-context
tags:
- system:sldb
- system:kgdb
- topic:semantic-export
- topic:execution
---

# Semantic export provenance task execution context

## What

_Define the context or guardrail this pill carries._

This task tightens the SLDB-to-KGDB handoff contract so downstream graph systems receive enough source-side provenance to reason globally without losing the chain back to authored textual units.

## Why

_Explain why this context matters for safe execution._

The repo already exports models, documents, sections, semantic tags, semantic DAG data, and hashes. The open question is whether that contract is explicit enough about document-subunit provenance once addressability, query, and composition become richer.

## When

_Describe when an agent should apply this pill._

Apply this pill when defining export provenance, deciding which source anchors must survive export, or clarifying the boundary between SLDB textual identity and downstream graph identity.

## Where

_Name the files, surfaces, or scope this pill applies to._

Read these first:

- `desk/tasks/task-tighten-semantic-export-provenance-contract.md`
- `desk/pills/pill-011-addressability-task-execution-context.md`
- `docs/architecture/semantic-export-boundary.md`
- `docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`
- `src/sldb/store/export.py`

Provenance that may need explicit handling:

- source document identity
- addressable textual unit identity when relevant
- model identity
- semantic tags
- extraction/hash lineage
- how downstream systems distinguish source anchors from graph-native identities

## How

_Describe the correct way to apply this guidance._

Use the addressability contract as the source-side truth. Preserve enough information that a downstream graph node or edge can be traced back to the authored document unit it came from without pretending the source anchor is itself a graph identity.

Produce a durable contract update that states:

- what provenance anchors are required
- which anchors are canonical versus derived
- what the export payload must preserve for downstream traceability
- whether new payload fields or clarified semantics are needed
- follow-up implementation tasks if payload changes should be staged

## How Not

_Describe the shortcut or failure mode to avoid._

Do not make KGDB depend on undocumented `.sldb` runtime internals, and do not collapse textual provenance anchors into graph-global ids.

