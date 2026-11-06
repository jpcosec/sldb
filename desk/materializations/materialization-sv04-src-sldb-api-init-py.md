---
id: materialization-sv04-src-sldb-api-init-py
title: 'SV04: src/sldb/api/__init__.py'
source_atoms:
- atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
target_kind: code
target_identity: src/sldb/api/__init__.py
validation:
- pytest -q tests/api/test_model_metadata_drafts.py
tags:
- system:sldb
- task:sv04
---

# SV04: src/sldb/api/__init__.py

## Intent

src/sldb/api/__init__.py materializa la decision de SV04 (atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill).
