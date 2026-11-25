---
sldb:
  by: agent
  at: '2026-11-25T06:10:13Z'
  authority: generated
  via: create_document
id: materialization-campo-default-src-sldb-runtime-validation-py
title: campo-default src-sldb-runtime-validation-py
source_atoms:
- atom-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes
target_kind: code
target_identity: src/sldb/runtime/validation.py
validation:
- pytest -q tests/test_campo_con_default.py
tags:
- system:sldb
- topic:campo-default
---

# campo-default src-sldb-runtime-validation-py

## Intent

materializa en src/sldb/runtime/validation.py el atom atom-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes
