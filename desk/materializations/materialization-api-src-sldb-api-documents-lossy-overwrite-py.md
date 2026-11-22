---
sldb:
  by: agent
  at: '2026-11-22T13:57:35Z'
  authority: generated
  via: create_document
id: materialization-api-src-sldb-api-documents-lossy-overwrite-py
title: api src-sldb-api-documents-lossy_overwrite-py
source_atoms:
- atom-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
target_kind: code
target_identity: src/sldb/api/documents/lossy_overwrite.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_lossy_overwrite_content.py
  tests/test_extraction_segments.py
tags:
- system:sldb
- topic:api
---

# api src-sldb-api-documents-lossy_overwrite-py

## Intent

materializa en src/sldb/api/documents/lossy_overwrite.py el atom atom-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
