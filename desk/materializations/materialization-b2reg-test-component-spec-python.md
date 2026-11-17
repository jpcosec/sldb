---
sldb:
  by: agent
  at: '2026-11-17T11:11:46Z'
  authority: generated
  via: create_document
id: materialization-b2reg-test-component-spec-python
title: b2reg test_component_spec_python
source_atoms:
- atom-el-spec-de-componentes-desde-python-lee-solo-archivos-py-aunque-el-árbol-tenga-otros-lenguajes
target_kind: test
target_identity: tests/notations/test_component_spec_python.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
tags:
- system:sldb
- topic:notations
---

# b2reg test_component_spec_python

## Intent

materializa en tests/notations/test_component_spec_python.py el atom atom-el-spec-de-componentes-desde-python-lee-solo-archivos-py-aunque-el-árbol-tenga-otros-lenguajes
