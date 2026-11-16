---
sldb:
  by: agent
  at: '2026-11-16T09:56:42Z'
  authority: generated
  via: create_document
id: materialization-portar-spec2viz-test-ported-from-spec2viz-view-contract-resolved
title: portar-spec2viz test_ported_from_spec2viz_view_contract_resolved
source_atoms:
- atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
target_kind: test
target_identity: tests/notations/test_ported_from_spec2viz_view_contract_resolved.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/
  -k ported_from_spec2viz
tags:
- system:sldb
- topic:notations
---

# portar-spec2viz test_ported_from_spec2viz_view_contract_resolved

## Intent

materializa en tests/notations/test_ported_from_spec2viz_view_contract_resolved.py el atom atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
