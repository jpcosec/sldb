---
sldb:
  by: agent
  at: '2026-11-25T06:11:10Z'
  authority: generated
  via: create_document
id: materialization-campo-default-tests-test-campo-con-default-py
title: campo-default tests-test_campo_con_default-py
source_atoms:
- atom-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes
target_kind: test
target_identity: tests/test_campo_con_default.py
validation:
- pytest -q tests/test_campo_con_default.py
tags:
- system:sldb
- topic:campo-default
---

# campo-default tests-test_campo_con_default-py

## Intent

materializa en tests/test_campo_con_default.py el atom atom-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes
