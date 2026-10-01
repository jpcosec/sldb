---
id: pill-007-sldb-text-layer-vs-kgdb-graph-layer
tags:
- system:sldb
- system:kgdb
- topic:architecture
- topic:semantic-export
---

# Keep SLDB as the text layer and KGDB as the graph layer

## What

_Define the context or guardrail this pill carries._

SLDB owns canonical readable documents, AST-like document structure, extraction, rendering, structural query, textual composition, and graph-ready export. KGDB owns graph-native persistence, traversal, equivalence, inference, and system-wide relational reasoning.

## Why

_Explain why this context matters for safe execution._

A stable boundary keeps authored textual truth separate from downstream graph truth and prevents duplicated feature ownership across the ecosystem.

## When

_Describe when an agent should apply this pill._

Apply this pill when a proposed feature touches composition, semantic export, global traversal, provenance, or cross-repo knowledge architecture.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md`
- semantic export surfaces
- downstream KGDB handoff design

## How

_Describe the correct way to apply this guidance._

Ask whether the feature is primarily about authored text and document structure or graph-native relations and reasoning. Keep text-first behavior in SLDB and graph-first behavior in KGDB.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not move textual authoring and rendering into KGDB, and do not turn SLDB into the graph-native reasoning engine.

