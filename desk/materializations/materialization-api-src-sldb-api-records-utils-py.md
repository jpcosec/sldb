---
sldb:
  by: agent
  at: '2026-11-21T13:23:36Z'
  authority: generated
  via: create_document
id: materialization-api-src-sldb-api-records-utils-py
title: api src-sldb-api-records-utils-py
source_atoms:
- atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
target_kind: code
target_identity: src/sldb/api/records/utils.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_models.py
  tests/api/test_model_metadata_drafts.py
tags:
- system:sldb
- topic:api
---

# api src-sldb-api-records-utils-py

## Intent

materializa en src/sldb/api/records/utils.py el atom atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
