---
sldb:
  by: agent
  at: '2026-11-21T07:30:56Z'
  authority: generated
  via: create_document
id: materialization-retiro-docs-architecture-spec2viz-python-ast-md
title: retiro docs-architecture-spec2viz-python-ast-md
source_atoms:
- atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
target_kind: docs
target_identity: docs/architecture/spec2viz/python-ast.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations
tags:
- system:sldb
- topic:retiro
---

# retiro docs-architecture-spec2viz-python-ast-md

## Intent

materializa en docs/architecture/spec2viz/python-ast.md el atom atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
