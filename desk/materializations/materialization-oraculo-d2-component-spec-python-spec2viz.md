---
sldb:
  by: agent
  at: '2026-11-16T09:32:01Z'
  authority: generated
  via: create_document
id: materialization-oraculo-d2-component-spec-python-spec2viz
title: oraculo-d2 component_spec_python_spec2viz
source_atoms:
- atom-la-paridad-de-d2-con-spec2viz-se-comprueba-contra-un-golden-congelado-no-contra-spec2viz-en-vivo
target_kind: test
target_identity: tests/notations/goldens/component_spec_python_spec2viz.json
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
tags:
- system:sldb
- topic:notations
---

# oraculo-d2 component_spec_python_spec2viz

## Intent

materializa en tests/notations/goldens/component_spec_python_spec2viz.json el atom atom-la-paridad-de-d2-con-spec2viz-se-comprueba-contra-un-golden-congelado-no-contra-spec2viz-en-vivo
