---
sldb:
  by: agent
  at: '2026-11-21T13:23:08Z'
  authority: generated
  via: create_document
id: materialization-api-src-sldb-api-model-registry-describe-model-py
title: api src-sldb-api-model_registry-describe_model-py
source_atoms:
- atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
target_kind: code
target_identity: src/sldb/api/model_registry/describe_model.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_models.py
  tests/api/test_model_metadata_drafts.py
tags:
- system:sldb
- topic:api
---

# api src-sldb-api-model_registry-describe_model-py

## Intent

materializa en src/sldb/api/model_registry/describe_model.py el atom atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
