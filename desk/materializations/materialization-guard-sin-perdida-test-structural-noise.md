---
sldb:
  by: agent
  at: '2026-11-19T14:26:53Z'
  authority: generated
  via: create_document
id: materialization-guard-sin-perdida-test-structural-noise
title: guard sin pérdida test_structural_noise
source_atoms:
- atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
target_kind: test
target_identity: tests/api/test_structural_noise.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py
tags:
- system:sldb
- topic:documents
---

# guard sin pérdida test_structural_noise

## Intent

materializa en tests/api/test_structural_noise.py el atom atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
