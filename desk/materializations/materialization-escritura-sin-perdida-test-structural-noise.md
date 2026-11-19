---
sldb:
  by: agent
  at: '2026-11-19T08:00:38Z'
  authority: generated
  via: create_document
id: materialization-escritura-sin-perdida-test-structural-noise
title: escritura sin perdida test_structural_noise
source_atoms:
- atom-una-escritura-por-campos-falla-antes-de-borrar-ruido-estructural-o-frontmatter-no-declarado-del-arch
target_kind: test
target_identity: tests/api/test_structural_noise.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py
tags:
- system:sldb
- topic:api
---

# escritura sin perdida test_structural_noise

## Intent

materializa en tests/api/test_structural_noise.py el atom atom-una-escritura-por-campos-falla-antes-de-borrar-ruido-estructural-o-frontmatter-no-declarado-del-arch
