---
sldb:
  by: agent
  at: '2026-11-21T13:27:05Z'
  authority: generated
  via: create_document
id: materialization-api-src-sldb-models-field-schema-descriptor-py
title: api src-sldb-models-field_schema-descriptor-py
source_atoms:
- atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
target_kind: code
target_identity: src/sldb/models/field_schema/descriptor.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_models.py
  tests/api/test_model_metadata_drafts.py
tags:
- system:sldb
- topic:api
---

# api src-sldb-models-field_schema-descriptor-py

## Intent

materializa en src/sldb/models/field_schema/descriptor.py el atom atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
