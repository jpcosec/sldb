---
sldb:
  by: agent
  at: '2026-11-16T09:58:34Z'
  authority: generated
  via: create_document
id: materialization-portar-spec2viz-component-exception-hierarchy
title: portar-spec2viz component-exception-hierarchy
source_atoms:
- atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
target_kind: test
target_identity: tests/notations/fixtures/docs/architecture/spec2viz/component-exception-hierarchy.yml
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/
  -k ported_from_spec2viz
tags:
- system:sldb
- topic:notations
---

# portar-spec2viz component-exception-hierarchy

## Intent

materializa en tests/notations/fixtures/docs/architecture/spec2viz/component-exception-hierarchy.yml el atom atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
