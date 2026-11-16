---
sldb:
  by: agent
  at: '2026-11-16T09:13:11Z'
  authority: generated
  via: create_document
id: materialization-go10-test-where-retired-contains-en-contexto-de-predicado
title: go10 test_where_retired contains en contexto de predicado
source_atoms:
- atom-en-el-código-de-docs-contains-es-el-operador-viejo-solo-en-contexto-de-predicado-solo-es-la-relación
target_kind: test
target_identity: tests/store/test_where_retired.py
validation:
- TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py
tags:
- system:sldb
- topic:rules-language
---

# go10 test_where_retired contains en contexto de predicado

## Intent

materializa en tests/store/test_where_retired.py la regla de que contains solo cuenta como operador viejo en contexto de predicado
