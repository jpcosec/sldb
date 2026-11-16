---
sldb:
  by: agent
  at: '2026-11-16T09:55:57Z'
  authority: generated
  via: create_document
id: materialization-portar-spec2viz-test-ported-from-spec2viz-notation-view
title: portar-spec2viz test_ported_from_spec2viz_notation_view
source_atoms:
- atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
target_kind: test
target_identity: tests/notations/test_ported_from_spec2viz_notation_view.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/
  -k ported_from_spec2viz
tags:
- system:sldb
- topic:notations
---

# portar-spec2viz test_ported_from_spec2viz_notation_view

## Intent

materializa en tests/notations/test_ported_from_spec2viz_notation_view.py el atom atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
