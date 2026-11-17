---
sldb:
  by: agent
  at: '2026-11-17T11:10:56Z'
  authority: generated
  via: create_document
id: materialization-b2reg-component-spec-python
title: b2reg component_spec_python
source_atoms:
- atom-el-spec-de-componentes-desde-python-lee-solo-archivos-py-aunque-el-árbol-tenga-otros-lenguajes
target_kind: code
target_identity: src/sldb/api/notations/component_spec_python.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
tags:
- system:sldb
- topic:notations
---

# b2reg component_spec_python

## Intent

materializa en src/sldb/api/notations/component_spec_python.py el atom atom-el-spec-de-componentes-desde-python-lee-solo-archivos-py-aunque-el-árbol-tenga-otros-lenguajes
