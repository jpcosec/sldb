---
sldb:
  by: agent
  at: '2026-11-19T10:59:38Z'
  authority: generated
  via: create_document
id: materialization-reindex-doc
title: reindex doc
source_atoms:
- atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
target_kind: code
target_identity: src/sldb/cli/commands/doc.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_api_documents.py
tags:
- system:sldb
- topic:cli
---

# reindex doc

## Intent

materializa en src/sldb/cli/commands/doc.py el atom atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force
