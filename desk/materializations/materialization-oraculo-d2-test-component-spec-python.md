---
sldb:
  by: agent
  at: '2026-11-16T09:31:39Z'
  authority: generated
  via: create_document
id: materialization-oraculo-d2-test-component-spec-python
title: oraculo-d2 test_component_spec_python
source_atoms:
- atom-la-paridad-de-d2-con-spec2viz-se-comprueba-contra-un-golden-congelado-no-contra-spec2viz-en-vivo
target_kind: test
target_identity: tests/notations/test_component_spec_python.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
tags:
- system:sldb
- topic:notations
---

# oraculo-d2 test_component_spec_python

## Intent

materializa en tests/notations/test_component_spec_python.py el atom atom-la-paridad-de-d2-con-spec2viz-se-comprueba-contra-un-golden-congelado-no-contra-spec2viz-en-vivo
