---
id: pill-003-template-marker-roundtrip-contract
tags:
- system:sldb
- topic:templates
- topic:roundtrip
- language:python
---

# Keep template markers reversible at the document boundary

## What

_Define the context or guardrail this pill carries._

Template marker features should preserve the reversible SLDB document contract unless a task explicitly defines a lossy representation.

## Why

_Explain why this context matters for safe execution._

Rendered values that cannot extract back into the same structured payload break the core promise that structured Markdown remains a safe source artifact.

## When

_Describe when an agent should apply this pill._

Apply this pill when changing marker families, render/extract behavior, standalone markers, or template invariant logic.

## Where

_Name the files, surfaces, or scope this pill applies to._

- `src/sldb/core/template_extractor.py`
- `src/sldb/core/data_extractor.py`
- text/list/yaml handlers
- marker roundtrip tests

## How

_Describe the correct way to apply this guidance._

Treat marker changes as bidirectional contract changes. Validate render and extract together and add focused tests for any new marker behavior.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not make rendering look nicer by silently weakening extraction fidelity or by introducing marker semantics that cannot roundtrip safely.

