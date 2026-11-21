---
sldb:
  by: agent
  at: '2026-11-21T13:24:07Z'
  authority: generated
  via: create_document
id: materialization-api-src-sldb-api-schema-field-descriptor-py
title: api src-sldb-api-schema-field_descriptor-py
source_atoms:
- atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
target_kind: code
target_identity: src/sldb/api/schema/field_descriptor.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_models.py
  tests/api/test_model_metadata_drafts.py
tags:
- system:sldb
- topic:api
---

# api src-sldb-api-schema-field_descriptor-py

## Intent

materializa en src/sldb/api/schema/field_descriptor.py el atom atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
