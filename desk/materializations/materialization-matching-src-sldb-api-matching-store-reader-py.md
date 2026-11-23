---
sldb:
  by: agent
  at: '2026-11-23T22:29:25Z'
  authority: generated
  via: create_document
id: materialization-matching-src-sldb-api-matching-store-reader-py
title: matching src-sldb-api-matching-store_reader-py
source_atoms:
- atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
target_kind: code
target_identity: src/sldb/api/matching/store_reader.py
validation:
- 'main limpio: pytest tests/matching/ tests/api/test_api_edges.py tests/store/test_live_stale_security.py
  58 passed; mutacion sin la cache de StoreReader: el test contador falla'
tags:
- system:sldb
- topic:matching
---

# matching src-sldb-api-matching-store_reader-py

## Intent

materializa en src/sldb/api/matching/store_reader.py el atom atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
