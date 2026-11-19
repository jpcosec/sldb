---
sldb:
  by: agent
  at: '2026-11-19T11:00:07Z'
  authority: generated
  via: create_document
id: materialization-reindex-docs1
title: reindex docs1
source_atoms:
- atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
target_kind: code
target_identity: src/sldb/cli/parsers/docs1.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_documents.py
tags:
- system:sldb
- topic:cli
---

# reindex docs1

## Intent

materializa en src/sldb/cli/parsers/docs1.py el atom atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
