---
sldb:
  by: agent
  at: '2026-11-21T07:30:23Z'
  authority: generated
  via: create_document
id: materialization-retiro-docs-architecture-code-docstring-indexing-handoff-md
title: retiro docs-architecture-code-docstring-indexing-handoff-md
source_atoms:
- atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
target_kind: docs
target_identity: docs/architecture/code-docstring-indexing-handoff.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations
tags:
- system:sldb
- topic:retiro
---

# retiro docs-architecture-code-docstring-indexing-handoff-md

## Intent

materializa en docs/architecture/code-docstring-indexing-handoff.md el atom atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
