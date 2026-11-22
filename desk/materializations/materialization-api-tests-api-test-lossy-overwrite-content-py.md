---
sldb:
  by: agent
  at: '2026-11-22T13:58:04Z'
  authority: generated
  via: create_document
id: materialization-api-tests-api-test-lossy-overwrite-content-py
title: api tests-api-test_lossy_overwrite_content-py
source_atoms:
- atom-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
target_kind: test
target_identity: tests/api/test_lossy_overwrite_content.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_lossy_overwrite_content.py
  tests/test_extraction_segments.py
tags:
- system:sldb
- topic:api
---

# api tests-api-test_lossy_overwrite_content-py

## Intent

materializa en tests/api/test_lossy_overwrite_content.py el atom atom-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda
