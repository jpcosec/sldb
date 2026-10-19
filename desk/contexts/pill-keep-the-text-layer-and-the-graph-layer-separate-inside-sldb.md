---
# pill-xxx
id: pill-keep-the-text-layer-and-the-graph-layer-separate-inside-sldb
status: active
summary: 'SLDB absorbió a KGDB: una sola base con dos capas internas, texto y grafo,
  que no se mezclan.'
# e.g., language:python, library:pydantic
tags:
- system:sldb
- topic:architecture
- topic:graph
---

# Keep the text layer and the graph layer separate inside SLDB

## What

_Define the context or guardrail this pill carries._

SLDB is one substrate with two internal layers. The text layer owns canonical readable documents, AST structure, extraction, rendering, structural query, textual composition and the semantic export. The graph layer (sldb.store.graph, the sldb graph commands) owns traversal, neighborhood, paths, equivalence and snapshots, derived from the edge index the store keeps. There is no external KGDB any more.

## Why

_Explain why this context matters for safe execution._

Authored text is the source of truth; the graph is derived from it. Keeping the layers apart inside one package stops the graph from becoming a second source of truth and keeps each feature owned by one layer.

## When

_Describe when an agent should apply this pill._

Apply when a change touches composition, the semantic export, graph traversal, edges, provenance or cross-repo knowledge architecture.

## Where

_Name the files, surfaces, or scope this pill applies to._

- docs/architecture/sldb-absorbs-kgdb.md
- src/sldb/store/graph/
- src/sldb/store/export.py and the sldb_semantic_export contract
- the sldb graph CLI

## How

_Describe the correct way to apply this guidance._

Ask whether the feature is about authored text and document structure or about relations derived from it. Text-first behavior goes in the text layer; graph-first behavior goes in sldb.store.graph and reads documents only through the store API.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not make the graph layer write documents or become a second source of truth, and do not read .sldb/runtime internals from outside the store API.
